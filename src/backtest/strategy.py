from __future__ import annotations

import pandas as pd


def signal_from_score(score: pd.Series, threshold: float = 70) -> pd.Series:
    return (score >= threshold).astype(int)
