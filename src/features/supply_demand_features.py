from __future__ import annotations

import pandas as pd


def build_supply_demand_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["margin_pressure"] = out["margin_buy_change_wow"].fillna(0) - out["margin_sell_change_wow"].fillna(0)
    out["short_squeeze_potential"] = out["short_interest_ratio"].fillna(0) * (1 - out["margin_ratio"].clip(lower=0) / 10)
    out["supply_demand_score"] = (
        50
        + 20 * out["short_squeeze_potential"].fillna(0)
        - 10 * out["margin_ratio"].fillna(0)
        + 15 * out["margin_pressure"].fillna(0)
    ).clip(0, 100)
    return out
