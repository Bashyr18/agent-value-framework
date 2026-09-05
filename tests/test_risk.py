from agent_value_framework.risk import RiskSignals, recommend_path, risk_band, risk_score


def test_zero_risk_green():
    score = risk_score(RiskSignals())
    assert score == 0
    assert risk_band(score) == "green"


def test_high_risk_red():
    score = risk_score(RiskSignals(ambiguity=1, blast_radius=1, coupling=1, domain_criticality=1, irreversibility=1, weak_verifiability=1))
    assert score == 1
    assert risk_band(score) == "red"
    assert recommend_path(score) == "strong-reasoning-before-mutation"
