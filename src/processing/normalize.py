from __future__ import annotations

import pandas as pd


def normalize_dates(df: pd.DataFrame, col: str) -> pd.DataFrame:
    out = df.copy()
    out[col] = pd.to_datetime(out[col]).dt.tz_localize(None)
    return out
