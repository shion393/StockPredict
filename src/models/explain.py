from __future__ import annotations

import pandas as pd


def top_feature_reasons(latest_row: pd.Series) -> list[str]:
    reasons: list[str] = []
    if latest_row.get("ma_gap_25", 0) > 0:
        reasons.append("25日移動平均線を上回って推移")
    if latest_row.get("supply_demand_score", 50) >= 55:
        reasons.append("需給指標が改善傾向")
    if latest_row.get("komatsu_business_score", 0) > 0:
        reasons.append("Komatsu月次事業指標が改善")
    if latest_row.get("news_quality_score", 50) < 40:
        reasons.append("ニュース品質スコアが弱く注意")
    return reasons[:3] or ["特徴量シグナルは中立"]
