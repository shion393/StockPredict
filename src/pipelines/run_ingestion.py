from __future__ import annotations

import argparse
from pathlib import Path

from src.ingestion.alpha_vantage import AlphaVantageSource
from src.ingestion.edinet import EdinetSource
from src.ingestion.jpx_margin import JpxMarginSource
from src.ingestion.jpx_short import JpxShortSource
from src.ingestion.komatsu_ir import KomatsuIRSource
from src.ingestion.news_api import NewsAPISource
from src.utils.dates import parse_date
from src.utils.io import write_parquet


def run_ingestion(start: str, end: str) -> None:
    s, e = parse_date(start), parse_date(end)
    root = Path("data/raw")
    write_parquet(AlphaVantageSource().fetch(s, e), root / "price.parquet")
    write_parquet(NewsAPISource().fetch(s, e), root / "news.parquet")
    write_parquet(EdinetSource().fetch(s, e), root / "edinet.parquet")
    write_parquet(JpxMarginSource().fetch(s, e), root / "jpx_margin.parquet")
    write_parquet(JpxShortSource().fetch(s, e), root / "jpx_short.parquet")
    write_parquet(KomatsuIRSource().fetch(s, e), root / "komatsu_ir.parquet")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    args = p.parse_args()
    run_ingestion(args.start, args.end)
