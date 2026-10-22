"""Settings model loaded from TOML."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class RenderSettings:
    box_color: tuple[int, int, int] = (0, 255, 120)
    text_color: tuple[int, int, int] = (255, 255, 255)
    show_distance: bool = True
    show_killer: bool = True
    max_distance_m: float = 60.0


@dataclass(frozen=True)
class Settings:
    version: str
    tick_interval_ms: int
    process_name: str
    render: RenderSettings
    hotkeys: dict[str, str] = field(default_factory=dict)


def load_settings(path: str | Path) -> Settings:
    p = Path(path)
    if not p.exists():
        return _defaults()
    with p.open("rb") as fh:
        raw = tomllib.load(fh)
    render = RenderSettings(**raw.get("render", {}))
    return Settings(
        version=raw.get("meta", {}).get("version", "0.9.3"),
        tick_interval_ms=raw.get("core", {}).get("tick_interval_ms", 16),
        process_name=raw.get("core", {}).get("process_name", "DeadByDaylight-Win64-Shipping.exe"),
        render=render,
        hotkeys=raw.get("hotkeys", {}),
    )


def _defaults() -> Settings:
    return Settings(
        version="0.9.3",
        tick_interval_ms=16,
        process_name="DeadByDaylight-Win64-Shipping.exe",
        render=RenderSettings(),
        hotkeys={"toggle_esp": "f1", "toggle_killer": "f2", "panic": "f12"},
    )