from __future__ import annotations

import pandas as pd
from sklearn.isotonic import IsotonicRegression


class ProbabilityCalibrator:
    def __init__(self) -> None:
        self.model = IsotonicRegression(out_of_bounds="clip")

    def fit(self, raw_prob: pd.Series, y_true: pd.Series) -> None:
        self.model.fit(raw_prob, y_true)

    def predict(self, raw_prob: pd.Series) -> pd.Series:
        out = self.model.predict(raw_prob)
        return pd.Series(out, index=raw_prob.index, name="buy_probability_calibrated")
