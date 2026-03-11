from src.models.predict import DecisionEngine


def test_decision_engine_avoids_negative_zero_expected_return():
    out = DecisionEngine().decide(prob_buy=0.5, expected_return=-0.0, risk_score=0.2, confidence=0.7)
    assert out["expected_excess_return"] == 0.0
