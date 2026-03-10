from __future__ import annotations

from src.serving.schemas import InferenceOutput


def format_output(payload: dict) -> InferenceOutput:
    return InferenceOutput(**payload)
