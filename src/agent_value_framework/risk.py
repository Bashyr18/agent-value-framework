from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True)
class RiskSignals:
    """Normalized task signals in [0,1]. Higher means more risk except where noted."""

    ambiguity: float = 0.0
    blast_radius: float = 0.0
    coupling: float = 0.0
    domain_criticality: float = 0.0
    irreversibility: float = 0.0
    weak_verifiability: float = 0.0

    def validate(self) -> None:
        for f in fields(self):
            value = getattr(self, f.name)
            if not 0 <= value <= 1:
                raise ValueError(f"{f.name} must be in [0, 1], got {value}")


DEFAULT_WEIGHTS = {
    "ambiguity": 0.20,
    "blast_radius": 0.20,
    "coupling": 0.15,
    "domain_criticality": 0.20,
    "irreversibility": 0.10,
    "weak_verifiability": 0.15,
}


def risk_score(signals: RiskSignals, weights: dict[str, float] | None = None) -> float:
    """Weighted risk score.

    The defaults are a starting policy, not empirical truth. Projects should
    tune them against their own accepted-change telemetry and failure history.
    """
    signals.validate()
    weights = weights or DEFAULT_WEIGHTS
    total_weight = sum(weights.values())
    if total_weight <= 0:
        raise ValueError("weights must sum to a positive number")
    numerator = 0.0
    for name, weight in weights.items():
        if not hasattr(signals, name):
            raise ValueError(f"unknown risk signal: {name}")
        if weight < 0:
            raise ValueError("weights cannot be negative")
        numerator += getattr(signals, name) * weight
    return numerator / total_weight


def risk_band(score: float, green_max: float = 0.35, amber_max: float = 0.65) -> str:
    if not 0 <= score <= 1:
        raise ValueError("score must be in [0, 1]")
    if score <= green_max:
        return "green"
    if score <= amber_max:
        return "amber"
    return "red"


def recommend_path(score: float, deterministic_verification: bool = True) -> str:
    band = risk_band(score)
    if band == "green":
        return "cheap-worker" if deterministic_verification else "cheap-worker+review"
    if band == "amber":
        return "orchestrator-plan->cheap-worker->gates"
    return "strong-reasoning-before-mutation"
