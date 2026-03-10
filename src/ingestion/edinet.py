from __future__ import annotations

from datetime import date

import pandas as pd

from src.ingestion.base import DataSource


class EdinetSource(DataSource):
    def fetch(self, start_date: date, end_date: date) -> pd.DataFrame:
        dates = pd.date_range(start_date, end_date, freq="QS")
        return pd.DataFrame(
            {
                "published_at": dates,
                "revenue_yoy": [0.03] * len(dates),
                "op_income_yoy": [0.04] * len(dates),
                "guidance_revision_flag": [0] * len(dates),
                "dividend_revision_flag": [0] * len(dates),
            }
        )
