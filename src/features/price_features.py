from __future__ import annotations

import pandas as pd


def _rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def _macd_hist(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    return macd - macd_signal


def build_price_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy().sort_values("date")
    out["ret_1"] = out["close"].pct_change(1)
    out["ret_5"] = out["close"].pct_change(5)
    out["ret_10"] = out["close"].pct_change(10)
    out["ma_5"] = out["close"].rolling(5).mean()
    out["ma_25"] = out["close"].rolling(25).mean()
    out["ma_gap_5"] = out["close"] / out["ma_5"] - 1
    out["ma_gap_25"] = out["close"] / out["ma_25"] - 1
    out["volatility_20"] = out["ret_1"].rolling(20).std()
    out["volume_spike"] = out["volume"] / out["volume"].rolling(20).mean()
    out["rsi_14"] = _rsi(out["close"], period=14)
    out["macd_hist"] = _macd_hist(out["close"])
    return out
