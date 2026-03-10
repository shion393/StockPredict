from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from src.ingestion.base import DataSource


class AlphaVantageSource(DataSource):
    """Stub source; replace with real API call in production."""

    def fetch(self, start_date: date, end_date: date) -> pd.DataFrame:
        dates = pd.bdate_range(start_date, end_date)
        rng = np.random.default_rng(42)
        close = 3000 + np.cumsum(rng.normal(0, 20, len(dates)))
        df = pd.DataFrame(
            {
                "date": dates,
                "open": close * (1 - 0.002),
                "high": close * (1 + 0.005),
                "low": close * (1 - 0.005),
                "close": close,
                "adjusted_close": close,
                "volume": rng.integers(2_000_000, 8_000_000, len(dates)),
            }
        )
        return df
