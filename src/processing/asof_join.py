from __future__ import annotations

import pandas as pd


def asof_join(left: pd.DataFrame, right: pd.DataFrame, left_on: str, right_on: str) -> pd.DataFrame:
    l = left.sort_values(left_on)
    r = right.sort_values(right_on)
    return pd.merge_asof(l, r, left_on=left_on, right_on=right_on, direction="backward")
