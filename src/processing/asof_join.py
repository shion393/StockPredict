from __future__ import annotations

import pandas as pd


def _normalize_datetime_key(df: pd.DataFrame, col: str) -> pd.DataFrame:
    out = df.copy()
    # pandas/pyarrow経由で datetime64[us] / datetime64[ms] が混在しても
    # merge_asof前に共通のdatetime64[ns]へ統一して比較可能にする
    out[col] = pd.to_datetime(out[col], utc=False).astype("datetime64[ns]")
    return out


def asof_join(left: pd.DataFrame, right: pd.DataFrame, left_on: str, right_on: str) -> pd.DataFrame:
    l = _normalize_datetime_key(left, left_on).sort_values(left_on)
    r = _normalize_datetime_key(right, right_on).sort_values(right_on)
    return pd.merge_asof(l, r, left_on=left_on, right_on=right_on, direction="backward")
