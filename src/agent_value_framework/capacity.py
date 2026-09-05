from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Iterable


class AvailabilityState(str, Enum):
    AVAILABLE = "available"
    EXHAUSTED = "exhausted"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class CapacityMode(str, Enum):
    NORMAL = "normal"
    CONSTRAINED = "constrained"
    RESERVE = "reserve"
    DEGRADED = "degraded"
    PAUSE_REQUIRED = "pause_required"


class FallbackSafety(str, Enum):
    SAFE = "fallback_safe"
    CONDITIONAL = "fallback_conditional"
    PROHIBITED = "fallback_prohibited"


class TransitionEvent(str, Enum):
    REGULAR_LIMIT_REACHED = "regular_limit_reached"
    CAPACITY_CONSTRAINED = "capacity_constrained"
    RESERVE_ENTERED = "reserve_entered"
    RESERVE_EXHAUSTED = "reserve_exhausted"
    REGULAR_CAPACITY_RESTORED = "regular_capacity_restored"
    MODEL_ROUTE_CHANGED = "model_route_changed"
    MODEL_ENTITLEMENT_LOST = "model_entitlement_lost"
    MODEL_ENTITLEMENT_GAINED = "model_entitlement_gained"
    CAPABILITY_MISMATCH = "capability_mismatch"
    RUNTIME_MODEL_MISMATCH = "runtime_model_mismatch"


@dataclass(frozen=True)
class CapacityPool:
    """A scarce pool with an optional project-assigned shadow price."""

    name: str
    shadow_price: float = 0.0
    expected_consumption: float = 0.0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("capacity pool name cannot be empty")
        for value, label in [
            (self.shadow_price, "shadow_price"),
            (self.expected_consumption, "expected_consumption"),
        ]:
            if not isfinite(value) or value < 0:
                raise ValueError(f"{label} must be finite and non-negative")

    @property
    def opportunity_cost(self) -> float:
        return self.shadow_price * self.expected_consumption


def capacity_opportunity_cost(pools: Iterable[CapacityPool]) -> float:
    """Return the user/project-supplied scarcity cost Σ(shadow price × use)."""
    return sum(pool.opportunity_cost for pool in pools)


@dataclass(frozen=True)
class CapacitySnapshot:
    """Runtime-supplied capacity facts; unknown values stay unknown."""

    regular: AvailabilityState = AvailabilityState.UNKNOWN
    reserve: AvailabilityState = AvailabilityState.UNKNOWN
    intended_model: str | None = None
    effective_model: str | None = None
    reset: str | None = None
    remaining: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "regular", AvailabilityState(self.regular))
        object.__setattr__(self, "reserve", AvailabilityState(self.reserve))
        if self.remaining is not None and (not isfinite(self.remaining) or not 0 <= self.remaining <= 1):
            raise ValueError("remaining must be normalized to [0, 1]")

    @property
    def routing_mismatch(self) -> bool:
        return bool(self.intended_model and self.effective_model and self.intended_model != self.effective_model)

    @property
    def mode(self) -> CapacityMode:
        return operating_mode(self)

    def to_dict(self) -> dict[str, object]:
        return {
            "effective_model": self.effective_model,
            "intended_model": self.intended_model,
            "mode": self.mode.value,
            "regular": self.regular.value,
            "remaining": self.remaining,
            "reset": self.reset,
            "reserve": self.reserve.value,
            "routing_mismatch": self.routing_mismatch,
        }


def operating_mode(snapshot: CapacitySnapshot, *, reserve_policy_allows: bool = True) -> CapacityMode:
    if snapshot.regular is AvailabilityState.AVAILABLE:
        return CapacityMode.DEGRADED if snapshot.routing_mismatch else CapacityMode.NORMAL
    if snapshot.regular in {AvailabilityState.EXHAUSTED, AvailabilityState.UNAVAILABLE}:
        if snapshot.reserve is AvailabilityState.AVAILABLE and reserve_policy_allows:
            return CapacityMode.RESERVE
        if snapshot.reserve in {AvailabilityState.EXHAUSTED, AvailabilityState.UNAVAILABLE}:
            return CapacityMode.PAUSE_REQUIRED
        return CapacityMode.CONSTRAINED
    return CapacityMode.DEGRADED if snapshot.routing_mismatch else CapacityMode.CONSTRAINED


@dataclass(frozen=True)
class RouteFeasibility:
    feasible: bool | None
    reasons: tuple[str, ...] = ()


def assess_route(
    *,
    entitlement: AvailabilityState = AvailabilityState.AVAILABLE,
    capacity: AvailabilityState = AvailabilityState.AVAILABLE,
    required_capabilities: Iterable[str] = (),
    available_capabilities: Iterable[str] = (),
    policy_allows: bool = True,
    hard_risk_override: bool = False,
    reserve: bool = False,
    reserve_allowed: bool = True,
    quality_floor_satisfied: bool | None = True,
) -> RouteFeasibility:
    entitlement = AvailabilityState(entitlement)
    capacity = AvailabilityState(capacity)
    reasons: list[str] = []
    unknown = False

    if entitlement is AvailabilityState.UNAVAILABLE:
        reasons.append("model_not_entitled")
    elif entitlement is AvailabilityState.UNKNOWN:
        reasons.append("entitlement_unknown")
        unknown = True

    if capacity is AvailabilityState.EXHAUSTED:
        reasons.append("capacity_exhausted")
    elif capacity is AvailabilityState.UNAVAILABLE:
        reasons.append("capacity_unavailable")
    elif capacity is AvailabilityState.UNKNOWN:
        reasons.append("capacity_unknown")
        unknown = True

    missing = sorted(set(required_capabilities) - set(available_capabilities))
    if missing:
        reasons.append("capability_mismatch:" + ",".join(missing))
    if not policy_allows:
        reasons.append("policy_prohibited")
    if hard_risk_override:
        reasons.append("hard_risk_override")
    if reserve and not reserve_allowed:
        reasons.append("reserve_route_prohibited")
    if quality_floor_satisfied is False:
        reasons.append("quality_floor_unsatisfied")
    elif quality_floor_satisfied is None:
        reasons.append("quality_floor_unknown")
        unknown = True

    if reasons and any(
        reason not in {"entitlement_unknown", "capacity_unknown", "quality_floor_unknown"}
        for reason in reasons
    ):
        return RouteFeasibility(False, tuple(reasons))
    if unknown:
        return RouteFeasibility(None, tuple(reasons))
    return RouteFeasibility(True, tuple(reasons))


def classify_fallback(
    *,
    risk_band: str,
    bounded: bool,
    high_risk: bool = False,
) -> FallbackSafety:
    """Classify remaining work before a restricted route is allowed to continue."""
    if high_risk or risk_band.lower() == "red":
        return FallbackSafety.PROHIBITED
    if risk_band.lower() == "green" and bounded:
        return FallbackSafety.SAFE
    return FallbackSafety.CONDITIONAL


def fallback_decision(
    safety: FallbackSafety,
    *,
    checkpointed: bool = False,
    contract_complete: bool = False,
) -> str:
    """Return the narrow action allowed by the fallback safety class."""
    safety = FallbackSafety(safety)
    if safety is FallbackSafety.SAFE:
        return "continue"
    if safety is FallbackSafety.CONDITIONAL and checkpointed and contract_complete:
        return "continue-after-reclassification"
    return "pause-required"
