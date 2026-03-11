import pandas as pd

from src.features.price_features import build_price_features


def test_price_features_include_rsi_and_macd_ranges():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=60, freq="B"),
            "close": [100 + i * 0.5 for i in range(60)],
            "volume": [1_000_000 + i * 1000 for i in range(60)],
        }
    )
    feat = build_price_features(df)
    assert "rsi_14" in feat.columns
    assert "macd_hist" in feat.columns
    assert feat["rsi_14"].between(0, 100).all()
