from __future__ import annotations

import pickle
from pathlib import Path

from src.features.labeler import make_excess_return_label, triple_barrier_label
from src.models.train_classifier import BuyClassifier
from src.models.train_regressor import ReturnRegressor
from src.utils.io import read_parquet


def run_training() -> None:
    df = read_parquet(Path("data/feature_store/features.parquet")).dropna().reset_index(drop=True)
    y_cls = triple_barrier_label(df["close"]).dropna()
    y_reg = make_excess_return_label(df).dropna()
    usable_idx = y_cls.index.intersection(y_reg.index)
    df = df.loc[usable_idx]
    y_cls = y_cls.loc[usable_idx]
    y_reg = y_reg.loc[usable_idx]

    cols = [
        "ret_1", "ret_5", "ret_10", "ma_gap_5", "ma_gap_25", "volatility_20", "volume_spike", "rsi_14", "macd_hist",
        "margin_ratio", "short_interest_ratio", "supply_demand_score", "fundamental_momentum",
        "komatsu_business_score", "news_quality_score",
    ]
    X = df[cols].fillna(0)

    cls = BuyClassifier()
    reg = ReturnRegressor()
    cls.fit(X, y_cls)
    reg.fit(X, y_reg)

    model_dir = Path("data/processed/models")
    model_dir.mkdir(parents=True, exist_ok=True)
    (model_dir / "features.txt").write_text("\n".join(cols), encoding="utf-8")
    with (model_dir / "classifier.pkl").open("wb") as fp:
        pickle.dump(cls, fp)
    with (model_dir / "regressor.pkl").open("wb") as fp:
        pickle.dump(reg, fp)


if __name__ == "__main__":
    run_training()
