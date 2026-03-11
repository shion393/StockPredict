from __future__ import annotations

import numpy as np
import pandas as pd


def _sanitize_zero(value: float) -> float:
    return 0.0 if abs(value) < 1e-12 else float(value)


class DecisionEngine:
    def decide(self, prob_buy: float, expected_return: float, risk_score: float, confidence: float) -> dict:
        prob_buy = float(np.clip(prob_buy, 0, 1))
        expected_return = _sanitize_zero(expected_return)
        risk_score = float(np.clip(risk_score, 0, 1))

        norm_return = float(np.clip((expected_return + 0.1) / 0.2, 0, 1))
        supply_demand_score = float(np.clip((1 - risk_score) * 100, 0, 100))
        news_quality_score = 50.0
        final_score = (
            0.45 * prob_buy * 100
            + 0.35 * norm_return * 100
            + 0.10 * supply_demand_score
            + 0.10 * news_quality_score
        )
        if final_score >= 70:
            decision = "BUY"
        elif final_score >= 45:
            decision = "WATCH"
        else:
            decision = "HOLD_OFF"
        return {
            "buy_score": round(float(final_score), 2),
            "decision": decision,
            "confidence": round(float(np.clip(confidence, 0, 1)), 3),
            "expected_excess_return": round(_sanitize_zero(expected_return), 4),
            "risk_score": round(float(risk_score), 4),
        }


def estimate_risk(df: pd.DataFrame) -> pd.Series:
    daily_vol = df["ret_1"].rolling(20).std()
    annualized_vol = daily_vol * np.sqrt(252)
    risk = (annualized_vol / 0.6).clip(0, 1).fillna(0.5)
    return risk.rename("risk_score")
