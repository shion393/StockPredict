from __future__ import annotations

import pandas as pd


def build_price_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy().sort_values("date")
    out["ret_1"] = out["close"].pct_change(1)
    out["ret_5"] = out["close"].pct_change(5)
    out["ret_10"] = out["close"].pct_change(10)
    out["ma_5"] = out["close"].rolling(5).mean()
    out["ma_25"] = out["close"].rolling(25).mean()
    out["ma_gap_5"] = out["close"] / out["ma_5"] - 1
    out["ma_gap_25"] = out["close"] / out["ma_25"] - 1
    out["volatility_20"] = out["ret_1"].rolling(20).std()
    out["volume_spike"] = out["volume"] / out["volume"].rolling(20).mean()
    return out
