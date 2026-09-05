from __future__ import annotations

from dataclasses import dataclass


class EconomicsError(ValueError):
    pass


def _probability(value: float, name: str) -> float:
    if not 0 < value <= 1:
        raise EconomicsError(f"{name} must be in (0, 1], got {value}")
    return value


@dataclass(frozen=True)
class TokenPrices:
    """USD per one million tokens."""

    input_per_million: float
    cached_input_per_million: float
    output_per_million: float

    def cost(self, *, input_tokens: int = 0, cached_input_tokens: int = 0, output_tokens: int = 0) -> float:
        if min(input_tokens, cached_input_tokens, output_tokens) < 0:
            raise EconomicsError("token counts cannot be negative")
        return (
            input_tokens / 1_000_000 * self.input_per_million
            + cached_input_tokens / 1_000_000 * self.cached_input_per_million
            + output_tokens / 1_000_000 * self.output_per_million
        )


@dataclass(frozen=True)
class AttemptEconomics:
    """Economics for a routing path before final acceptance.

    All monetary values are direct dollars. `accept_probability` should come
    from project telemetry/evals when available, not from a benchmark score.
    """

    base_cost: float
    verification_cost: float = 0.0
    expected_tool_cost: float = 0.0
    expected_review_cost: float = 0.0
    expected_escalation_cost: float = 0.0
    expected_rework_cost: float = 0.0
    accept_probability: float = 1.0

    @property
    def expected_attempt_cost(self) -> float:
        return sum(
            (
                self.base_cost,
                self.verification_cost,
                self.expected_tool_cost,
                self.expected_review_cost,
                self.expected_escalation_cost,
                self.expected_rework_cost,
            )
        )

    @property
    def ecac(self) -> float:
        """Expected Cost per Accepted Change under a stationary retry approximation."""
        p = _probability(self.accept_probability, "accept_probability")
        return self.expected_attempt_cost / p


def empirical_ecac(total_spend: float, accepted_changes: int) -> float:
    """The preferred metric once real workflow telemetry exists."""
    if total_spend < 0:
        raise EconomicsError("total_spend cannot be negative")
    if accepted_changes <= 0:
        raise EconomicsError("accepted_changes must be positive")
    return total_spend / accepted_changes


def upgrade_break_even_loss(
    *,
    cheap_cost: float,
    premium_cost: float,
    cheap_failure_probability: float,
    premium_failure_probability: float,
) -> float:
    """Return the downstream failure loss at which the premium route pays for itself.

    Derivation:
        premium_cost + p_premium * L <= cheap_cost + p_cheap * L
        L >= (premium_cost - cheap_cost) / (p_cheap - p_premium)

    If the premium route is not safer, no finite positive break-even exists.
    """
    for value, name in [
        (cheap_failure_probability, "cheap_failure_probability"),
        (premium_failure_probability, "premium_failure_probability"),
    ]:
        if not 0 <= value <= 1:
            raise EconomicsError(f"{name} must be in [0, 1]")
    delta_p = cheap_failure_probability - premium_failure_probability
    delta_cost = premium_cost - cheap_cost
    if delta_p <= 0:
        raise EconomicsError("premium route must have a lower failure probability")
    if delta_cost <= 0:
        return 0.0
    return delta_cost / delta_p


def expected_escalation_cost(probability: float, cost_if_triggered: float) -> float:
    if not 0 <= probability <= 1:
        raise EconomicsError("probability must be in [0, 1]")
    if cost_if_triggered < 0:
        raise EconomicsError("cost_if_triggered cannot be negative")
    return probability * cost_if_triggered
