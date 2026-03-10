from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd
from lightgbm import LGBMClassifier


class ModelTrainer(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        raise NotImplementedError

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series:
        raise NotImplementedError


class BuyClassifier(ModelTrainer):
    def __init__(self) -> None:
        self.model = LGBMClassifier(n_estimators=300, learning_rate=0.03, random_state=42)

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> pd.Series:
        proba = self.model.predict_proba(X)[:, 1]
        return pd.Series(proba, index=X.index, name="buy_probability")
