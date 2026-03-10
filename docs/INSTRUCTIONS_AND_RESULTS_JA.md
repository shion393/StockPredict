# コマツ買い時判定AI: インストラクション & コード説明ページ

このページは、リポジトリを GitHub にアップしたあとにそのまま参照できる「利用説明ページ」です。  
目的は次の3点です。

1. 何を実行すればよいか（運用手順）
2. コードがどこで何をしているか（構成説明）
3. 出力結果をどう読むか（解釈ルール）

---

## 1. まず何を実行すればよいか

最短ルートは以下です。

```bash
python -m src.pipelines.run_ingestion --start 2020-01-01 --end 2024-12-31
python -m src.pipelines.run_features --start 2020-01-01 --end 2024-12-31
python -m src.pipelines.run_training
python -m src.pipelines.run_inference --asof 2026-03-10
```

### 各コマンドの意味

- `run_ingestion`
  - 価格・ニュース・EDINET・JPX・Komatsu IR の raw データを取得して `data/raw/` に保存。
- `run_features`
  - raw データを時系列結合・特徴量化し、`data/feature_store/features.parquet` を作成。
- `run_training`
  - 学習データを作り、分類器・回帰器を学習して `data/processed/models/` に保存。
- `run_inference`
  - 最新時点の 1 レコードを推論し、`buy_score` / `decision` / `confidence` を JSON 出力。

---

## 2. コード構成（どこを見ればよいか）

### パイプライン入口

- `src/pipelines/run_ingestion.py`:
  - データ取得の入口
- `src/pipelines/run_features.py`:
  - 特徴量生成の入口
- `src/pipelines/run_training.py`:
  - モデル学習の入口
- `src/pipelines/run_backtest.py`:
  - バックテストの入口
- `src/pipelines/run_inference.py`:
  - 日次推論の入口

### 中核ロジック

- 取得アダプタ: `src/ingestion/*.py`
- 時系列結合: `src/processing/asof_join.py`
- 特徴量: `src/features/*.py`
- ラベル生成: `src/features/labeler.py`
- モデル: `src/models/train_classifier.py`, `src/models/train_regressor.py`
- スコア判定: `src/models/predict.py`
- 出力スキーマ: `src/serving/schemas.py`

### 単体実行のメイン

- `src/main.py` は `run_inference` を呼ぶラッパーで、
  「as-of 日付を指定して 1 回推論する」用途です。

---

## 3. 結果の見方（重要）

`run_inference` の出力例:

```json
{
  "as_of_date": "2026-03-10",
  "ticker": "6301.T",
  "horizon_days": 10,
  "buy_score": 74.2,
  "decision": "BUY",
  "confidence": 0.68,
  "expected_excess_return": 0.031,
  "risk_score": 0.41,
  "top_reasons": ["..."],
  "warnings": ["..."],
  "feature_snapshot": {"...": 0.0}
}
```

### 意味

- `buy_score` (0〜100)
  - 総合評価。高いほど買い優位。
- `decision`
  - `BUY` / `WATCH` / `HOLD_OFF` の3段階。
- `confidence` (0〜1)
  - 今回判定の信頼度目安。
- `expected_excess_return`
  - ベンチマーク差分の期待超過リターン。
- `risk_score` (0〜1)
  - 値動きリスクの目安。高いほどリスク大。
- `top_reasons`
  - 判定理由の上位説明。
- `warnings`
  - 決算前・ニュース変動などの注意点。
- `feature_snapshot`
  - 主要特徴量のその日の値。

### 実務での解釈ルール（推奨）

- `BUY` でも **confidence が低い場合は見送り** を検討。
- `WATCH` は「即買い」ではなく、翌日以降の継続監視対象。
- `HOLD_OFF` でも、イベント通過後にスコアが急回復するケースがあるため再評価する。
- `warnings` が出ている日は、通常よりポジションサイズを落とす。

---

## 4. よくあるエラーと対処

- `features.parquet が無い`
  - `run_features` を先に実行。
- `classifier.pkl / regressor.pkl が無い`
  - `run_training` を先に実行。
- `asof join の列重複エラー`
  - `asof_join` 側で重複列除外・日時型統一の処理が入っている最新版を利用。

---

## 5. GitHub公開時のおすすめ

- このファイルを `docs/` に置いたまま公開すると、
  新規メンバーが README からすぐに利用手順・結果解釈まで辿れます。
- 将来的に、実データ接続版（APIキー必須）とモック版（開発用）を章分けすると運用しやすくなります。
