from __future__ import annotations

import pandas as pd

from src.backtest.metrics import compute_metrics
from src.backtest.strategy import signal_from_score


def run_backtest(df: pd.DataFrame) -> dict:
    signal = signal_from_score(df["buy_score"])
    strat_ret = signal.shift(1).fillna(0) * df["ret_1"].fillna(0)
    return compute_metrics(strat_ret)
