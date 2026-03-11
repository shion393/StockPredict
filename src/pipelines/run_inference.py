from __future__ import annotations

import pickle
from pathlib import Path

from src.models.explain import top_feature_reasons
from src.models.predict import DecisionEngine, estimate_risk
from src.serving.schemas import InferenceOutput
from src.settings import Settings
from src.utils.io import read_parquet


def run_inference(asof: str) -> InferenceOutput:
    cfg = Settings.load().base
    ticker = cfg["project"]["ticker"]
    horizon = cfg["horizon"]["prediction_days"]

    feat = read_parquet(Path("data/feature_store/features.parquet")).dropna().reset_index(drop=True)
    latest = feat.iloc[-1]
    model_dir = Path("data/processed/models")
    cols = (model_dir / "features.txt").read_text(encoding="utf-8").splitlines()
    with (model_dir / "classifier.pkl").open("rb") as fp:
        cls = pickle.load(fp)
    with (model_dir / "regressor.pkl").open("rb") as fp:
        reg = pickle.load(fp)

    x = feat[cols].tail(1).fillna(0)
    prob = float(cls.predict(x).iloc[0])
    exp = float(reg.predict(x).iloc[0])
    risk = float(estimate_risk(feat).iloc[-1])
    confidence = max(prob, 1 - prob) * (1 - min(risk, 0.8) * 0.4)
    decision = DecisionEngine().decide(prob, exp, risk, confidence)

    return InferenceOutput(
        as_of_date=asof,
        ticker=ticker,
        horizon_days=horizon,
        buy_score=decision["buy_score"],
        decision=decision["decision"],
        confidence=decision["confidence"],
        expected_excess_return=decision["expected_excess_return"],
        risk_score=decision["risk_score"],
        top_reasons=top_feature_reasons(latest),
        warnings=["決算発表や重要イベント近辺の変動に注意"],
        feature_snapshot={
            "rsi_14": float(latest.get("rsi_14", 50)),
            "macd_hist": float(latest.get("macd_hist", 0)),
            "margin_ratio": float(latest.get("margin_ratio", 0)),
            "short_interest_ratio": float(latest.get("short_interest_ratio", 0)),
            "bb_ratio_mining": float(latest.get("bb_ratio_mining", 0)),
        },
    )


if __name__ == "__main__":
    print(run_inference("2026-03-10").model_dump_json(indent=2, ensure_ascii=False))
