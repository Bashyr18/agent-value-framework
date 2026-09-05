import pytest

from agent_value_framework.capacity import (
    AvailabilityState,
    CapacityMode,
    CapacityPool,
    CapacitySnapshot,
    FallbackSafety,
    assess_route,
    capacity_opportunity_cost,
    classify_fallback,
    fallback_decision,
)


def test_capacity_modes_keep_unknown_explicit():
    assert CapacitySnapshot(regular=AvailabilityState.AVAILABLE).mode is CapacityMode.NORMAL
    assert CapacitySnapshot(regular=AvailabilityState.EXHAUSTED, reserve=AvailabilityState.AVAILABLE).mode is CapacityMode.RESERVE
    assert CapacitySnapshot(regular=AvailabilityState.EXHAUSTED, reserve=AvailabilityState.EXHAUSTED).mode is CapacityMode.PAUSE_REQUIRED
    assert CapacitySnapshot(regular=AvailabilityState.EXHAUSTED).mode is CapacityMode.CONSTRAINED


def test_capacity_mismatch_is_not_reserve_proof():
    snapshot = CapacitySnapshot(regular=AvailabilityState.AVAILABLE, intended_model="sol", effective_model="luna")
    assert snapshot.routing_mismatch
    assert snapshot.mode is CapacityMode.DEGRADED
    assert snapshot.reserve is AvailabilityState.UNKNOWN


def test_capacity_pool_cost_is_project_defined():
    pools = [CapacityPool("reserve", shadow_price=2, expected_consumption=3), CapacityPool("tokens", 1, 4)]
    assert capacity_opportunity_cost(pools) == 10
    with pytest.raises(ValueError):
        CapacityPool("reserve", shadow_price=-1)


def test_route_feasibility_is_tri_state_and_structured():
    assert assess_route().feasible is True
    assert assess_route(entitlement=AvailabilityState.UNKNOWN).feasible is None
    assert assess_route(capacity=AvailabilityState.EXHAUSTED).feasible is False
    assert "capability_mismatch:browser" in assess_route(required_capabilities=["browser"], available_capabilities=[]).reasons


def test_quality_and_policy_constraints_override_price():
    result = assess_route(quality_floor_satisfied=False, policy_allows=True)
    assert result.feasible is False
    assert "quality_floor_unsatisfied" in result.reasons
    assert assess_route(reserve=True, reserve_allowed=False).feasible is False
    assert assess_route(hard_risk_override=True).feasible is False


def test_fallback_policy_requires_a_bounded_contract():
    assert classify_fallback(risk_band="green", bounded=True) is FallbackSafety.SAFE
    assert fallback_decision(FallbackSafety.SAFE) == "continue"
    assert classify_fallback(risk_band="amber", bounded=True) is FallbackSafety.CONDITIONAL
    assert fallback_decision(FallbackSafety.CONDITIONAL) == "pause-required"
    assert fallback_decision(FallbackSafety.CONDITIONAL, checkpointed=True, contract_complete=True) == "continue-after-reclassification"
    assert classify_fallback(risk_band="red", bounded=True) is FallbackSafety.PROHIBITED
