from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.features.fundamentals_features import build_fundamental_features
from src.features.komatsu_features import build_komatsu_specific_features
from src.features.news_features import build_news_features
from src.features.price_features import build_price_features
from src.features.supply_demand_features import build_supply_demand_features
from src.processing.asof_join import asof_join
from src.utils.io import read_parquet, write_parquet


def _build_benchmark_from_price(price: pd.DataFrame) -> pd.Series:
    ret = price["close"].pct_change().fillna(0)
    bench_ret = (ret * 0.65).rolling(5, min_periods=1).mean()
    return price["close"].iloc[0] * (1 + bench_ret).cumprod()


def run_features(start: str | None = None, end: str | None = None) -> pd.DataFrame:
    raw = Path("data/raw")
    price = read_parquet(raw / "price.parquet")
    price["benchmark_close"] = _build_benchmark_from_price(price)
    news = read_parquet(raw / "news.parquet")
    edinet = read_parquet(raw / "edinet.parquet")
    margin = read_parquet(raw / "jpx_margin.parquet")
    short = read_parquet(raw / "jpx_short.parquet")
    komatsu = read_parquet(raw / "komatsu_ir.parquet")

    feat = build_price_features(price)
    for df in (margin, short, edinet, komatsu):
        feat = asof_join(feat, df, "date", "published_at")

    feat = build_supply_demand_features(feat)
    feat = build_fundamental_features(feat)
    feat = build_komatsu_specific_features(feat)
    news_feat = build_news_features(news, feat[["date"]])
    feat = feat.merge(news_feat, on="date", how="left")
    write_parquet(feat, Path("data/feature_store/features.parquet"))
    return feat


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=False)
    parser.add_argument("--end", required=False)
    args = parser.parse_args()
    run_features(args.start, args.end)
