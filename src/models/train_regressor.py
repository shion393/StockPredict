from __future__ import annotations

import pandas as pd
from lightgbm import LGBMRegressor


class ReturnRegressor:
    def __init__(self) -> None:
        self.model = LGBMRegressor(n_estimators=300, learning_rate=0.03, random_state=42)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pred = self.model.predict(X)
        return pd.Series(pred, index=X.index, name="expected_excess_return")
