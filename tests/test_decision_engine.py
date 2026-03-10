from src.models.predict import DecisionEngine


def test_decision_engine_thresholds():
    eng = DecisionEngine()
    buy = eng.decide(prob_buy=0.9, expected_return=0.06, risk_score=0.2, confidence=0.9)
    hold = eng.decide(prob_buy=0.1, expected_return=-0.05, risk_score=0.8, confidence=0.2)
    assert buy["decision"] == "BUY"
    assert hold["decision"] == "HOLD_OFF"
