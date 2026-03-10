from __future__ import annotations

import argparse

from src.pipelines.run_inference import run_inference


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Komatsu buy decision inference")
    parser.add_argument("--asof", required=True, help="as-of date (YYYY-MM-DD)")
    args = parser.parse_args()
    result = run_inference(args.asof)
    print(result.model_dump_json(indent=2, ensure_ascii=False))
