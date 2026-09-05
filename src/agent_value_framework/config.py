from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from .math import TokenPrices


@dataclass(frozen=True)
class ModelEntry:
    name: str
    model: str
    effort: str
    prices: TokenPrices


def load_toml(path: str | Path) -> dict:
    with Path(path).open("rb") as f:
        return tomllib.load(f)


def load_models(path: str | Path) -> dict[str, ModelEntry]:
    data = load_toml(path)
    result: dict[str, ModelEntry] = {}
    for name, cfg in data.get("models", {}).items():
        pricing = cfg.get("pricing", {})
        result[name] = ModelEntry(
            name=name,
            model=cfg["model"],
            effort=cfg.get("effort", "medium"),
            prices=TokenPrices(
                input_per_million=float(pricing["input"]),
                cached_input_per_million=float(pricing.get("cached_input", pricing["input"])),
                output_per_million=float(pricing["output"]),
            ),
        )
    return result
