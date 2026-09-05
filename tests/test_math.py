import math
import pytest

from agent_value_framework.math import AttemptEconomics, TokenPrices, empirical_ecac, upgrade_break_even_loss


def test_token_prices():
    p = TokenPrices(0.2, 0.02, 1.2)
    assert math.isclose(p.cost(input_tokens=1_000_000, cached_input_tokens=1_000_000, output_tokens=1_000_000), 1.42)


def test_ecac_stationary():
    e = AttemptEconomics(base_cost=0.30, verification_cost=0.05, accept_probability=0.70)
    assert math.isclose(e.expected_attempt_cost, 0.35)
    assert math.isclose(e.ecac, 0.5)


def test_empirical_ecac():
    assert empirical_ecac(10, 20) == 0.5


def test_break_even():
    value = upgrade_break_even_loss(cheap_cost=0.3, premium_cost=1.2, cheap_failure_probability=0.2, premium_failure_probability=0.05)
    assert math.isclose(value, 6.0)


def test_break_even_requires_safer_premium():
    with pytest.raises(ValueError):
        upgrade_break_even_loss(cheap_cost=0.3, premium_cost=1.2, cheap_failure_probability=0.05, premium_failure_probability=0.2)
