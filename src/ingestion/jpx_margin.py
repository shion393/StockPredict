from __future__ import annotations

from datetime import date

import pandas as pd

from src.ingestion.base import DataSource


class JpxMarginSource(DataSource):
    def fetch(self, start_date: date, end_date: date) -> pd.DataFrame:
        dates = pd.date_range(start_date, end_date, freq="W-WED")
        return pd.DataFrame(
            {
                "published_at": dates,
                "margin_buy_balance": 1_000_000,
                "margin_sell_balance": 400_000,
                "margin_ratio": 2.5,
                "margin_buy_change_wow": 0.01,
                "margin_sell_change_wow": -0.02,
            }
        )
