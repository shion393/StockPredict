from __future__ import annotations

from datetime import date

import pandas as pd

from src.ingestion.base import DataSource


class NewsAPISource(DataSource):
    def fetch(self, start_date: date, end_date: date) -> pd.DataFrame:
        dates = pd.bdate_range(start_date, end_date)
        return pd.DataFrame(
            {
                "published_at": dates,
                "source": "mock",
                "title": "Komatsu update",
                "description": "Mocked article",
                "url": "https://example.com",
                "language": "ja",
                "article_type": "general",
                "sentiment_score": 0.1,
                "event_tag": "none",
            }
        )
