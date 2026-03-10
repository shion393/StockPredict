from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Settings:
    root: Path
    base: dict[str, Any]
    data_sources: dict[str, Any]
    model: dict[str, Any]

    @classmethod
    def load(cls, root: Path | None = None) -> "Settings":
        root = root or Path(__file__).resolve().parents[1]
        configs = root / "configs"
        return cls(
            root=root,
            base=_load_yaml(configs / "base.yaml"),
            data_sources=_load_yaml(configs / "data_sources.yaml"),
            model=_load_yaml(configs / "model.yaml"),
        )


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)
