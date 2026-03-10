from __future__ import annotations

import numpy as np
import pandas as pd


def make_excess_return_label(df: pd.DataFrame, horizon_days: int = 10) -> pd.Series:
    fwd = df["close"].shift(-horizon_days) / df["close"] - 1
    bench = df["benchmark_close"].shift(-horizon_days) / df["benchmark_close"] - 1
    return (fwd - bench).rename("target_excess_return")


def triple_barrier_label(close: pd.Series, up: float = 0.05, down: float = -0.03, horizon_days: int = 10) -> pd.Series:
    labels = np.full(len(close), np.nan)
    values = close.values
    for i in range(len(close) - horizon_days):
        window = values[i + 1 : i + horizon_days + 1] / values[i] - 1
        up_hit = np.where(window >= up)[0]
        down_hit = np.where(window <= down)[0]
        if len(up_hit) and (not len(down_hit) or up_hit[0] < down_hit[0]):
            labels[i] = 1
        elif len(down_hit) and (not len(up_hit) or down_hit[0] < up_hit[0]):
            labels[i] = 0
        else:
            labels[i] = int(window[-1] > 0)
    return pd.Series(labels, index=close.index, name="target_buy_label")
