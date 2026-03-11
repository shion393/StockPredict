# Komatsu Buy AI (6301.T)

コマツ（6301.T）の5〜20営業日スイング向け買い時を、日次で判定する判定支援AIの実装雛形です。

## What it does
- 株価・需給・業績・コマツ固有IR・ニュースを統合する拡張可能なモジュール構成
- LightGBM分類/回帰を併用し、`buy_score (0-100)` と `BUY/WATCH/HOLD_OFF` を出力
- 公表日基準のas-of結合でリークを抑制
- 学習・バックテスト・日次推論のCLIエントリを提供

## Quick start
```bash
python -m src.pipelines.run_ingestion --start 2020-01-01 --end 2024-12-31
python -m src.pipelines.run_features --start 2020-01-01 --end 2024-12-31
python -m src.pipelines.run_training
python -m src.pipelines.run_backtest
python -m src.pipelines.run_inference --asof 2026-03-10
```

## Output schema
`src/serving/schemas.py` にPydanticスキーマを定義。

## ドキュメント（利用手順と結果の見方）
- 詳細ガイド: `docs/INSTRUCTIONS_AND_RESULTS_JA.md`


## Notes
- JPX/Komatsu IR はExcel/CSV/HTML公開が混在するため、adapter実装を差し替え可能にしています。
- このリポジトリは最小実装です。実運用時は監視・リトライ・認証・データ品質ゲートを強化してください。
