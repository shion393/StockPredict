from __future__ import annotations

import numpy as np
import pandas as pd


class DecisionEngine:
    def decide(self, prob_buy: float, expected_return: float, risk_score: float, confidence: float) -> dict:
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
            "confidence": round(float(confidence), 3),
            "expected_excess_return": round(float(expected_return), 4),
            "risk_score": round(float(risk_score), 4),
        }


def estimate_risk(df: pd.DataFrame) -> pd.Series:
    return df["ret_1"].rolling(20).std().fillna(0).clip(0, 1).rename("risk_score")
