from __future__ import annotations

import json
import pickle
from pathlib import Path

from src.backtest.engine import run_backtest
from src.models.predict import DecisionEngine, estimate_risk
from src.utils.io import read_parquet


def run_backtest_pipeline() -> dict:
    feat = read_parquet(Path("data/feature_store/features.parquet")).dropna().reset_index(drop=True)
    model_dir = Path("data/processed/models")
    cols = (model_dir / "features.txt").read_text(encoding="utf-8").splitlines()
    with (model_dir / "classifier.pkl").open("rb") as fp:
        cls = pickle.load(fp)
    with (model_dir / "regressor.pkl").open("rb") as fp:
        reg = pickle.load(fp)
    X = feat[cols].fillna(0)
    p = cls.predict(X)
    r = reg.predict(X)
    risk = estimate_risk(feat)
    engine = DecisionEngine()
    feat["buy_score"] = [engine.decide(pp, rr, rk, pp)["buy_score"] for pp, rr, rk in zip(p, r, risk)]
    result = run_backtest(feat)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    (Path("data/processed") / "backtest_metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(run_backtest_pipeline())
