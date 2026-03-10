from __future__ import annotations

from pydantic import BaseModel


class InferenceOutput(BaseModel):
    as_of_date: str
    ticker: str
    horizon_days: int
    buy_score: float
    decision: str
    confidence: float
    expected_excess_return: float
    risk_score: float
    top_reasons: list[str]
    warnings: list[str]
    feature_snapshot: dict[str, float]
