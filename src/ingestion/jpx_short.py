from __future__ import annotations

from datetime import date

import pandas as pd

from src.ingestion.base import DataSource


class JpxShortSource(DataSource):
    def fetch(self, start_date: date, end_date: date) -> pd.DataFrame:
        dates = pd.bdate_range(start_date, end_date)
        return pd.DataFrame(
            {
                "published_at": dates,
                "short_interest_ratio": 0.7,
                "short_interest_change": 0.0,
                "lending_restriction_flag": 0,
                "daily_publication_flag": 1,
            }
        )
