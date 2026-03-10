from __future__ import annotations

import pandas as pd


def compute_metrics(returns: pd.Series) -> dict:
    equity = (1 + returns.fillna(0)).cumprod()
    drawdown = equity / equity.cummax() - 1
    return {
        "total_return": float(equity.iloc[-1] - 1),
        "win_rate": float((returns > 0).mean()),
        "max_drawdown": float(drawdown.min()),
        "trades": int((returns != 0).sum()),
    }
