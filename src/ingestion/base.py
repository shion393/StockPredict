from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

import pandas as pd


class DataSource(ABC):
    @abstractmethod
    def fetch(self, start_date: date, end_date: date) -> pd.DataFrame:
        raise NotImplementedError
