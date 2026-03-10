from __future__ import annotations

import pandas as pd


def build_komatsu_specific_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["komatsu_business_score"] = (
        40 * out["demand_growth_7_regions"].fillna(0)
        + 25 * (out["bb_ratio_mining"].fillna(1) - 1)
        + 35 * out["komtrax_yoy"].fillna(0)
    )
    return out
