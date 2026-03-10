from __future__ import annotations

import pandas as pd


def build_fundamental_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["fundamental_momentum"] = (
        out["revenue_yoy"].fillna(0) * 0.4
        + out["op_income_yoy"].fillna(0) * 0.6
        - out["guidance_revision_flag"].fillna(0) * 0.1
    )
    return out
