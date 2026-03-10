from __future__ import annotations

import pandas as pd


def build_news_features(news_df: pd.DataFrame, calendar: pd.DataFrame) -> pd.DataFrame:
    n = news_df.copy()
    n["date"] = pd.to_datetime(n["published_at"]).dt.normalize()
    daily = n.groupby("date").agg(news_count=("title", "count"), sentiment=("sentiment_score", "mean")).reset_index()
    out = calendar[["date"]].merge(daily, on="date", how="left").fillna({"news_count": 0, "sentiment": 0})
    out["news_count_3d"] = out["news_count"].rolling(3).sum()
    out["news_count_7d"] = out["news_count"].rolling(7).sum()
    out["news_quality_score"] = (50 + out["sentiment"] * 20 - (out["news_count_7d"] > 25) * 10).clip(0, 100)
    return out
