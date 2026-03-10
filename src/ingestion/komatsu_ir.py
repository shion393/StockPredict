from __future__ import annotations

from datetime import date

import pandas as pd

from src.ingestion.base import DataSource


class KomatsuIRSource(DataSource):
    def fetch(self, start_date: date, end_date: date) -> pd.DataFrame:
        dates = pd.date_range(start_date, end_date, freq="MS")
        return pd.DataFrame(
            {
                "published_at": dates,
                "demand_growth_7_regions": 0.02,
                "bb_ratio_mining": 1.1,
                "komtrax_hours_by_region": 0.03,
                "komtrax_yoy": 0.04,
                "demand_update_flag": 1,
                "management_event_flag": 0,
            }
        )
