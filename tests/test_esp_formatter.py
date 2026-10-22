"""Unit tests for the ESP formatter — no game process required."""
from __future__ import annotations

from src.config.settings import RenderSettings, Settings
from src.models.actor import Actor, ActorRole
from src.processors.esp_formatter import EspFormatter


def _settings(show_killer: bool = True, max_dist: float = 60.0) -> Settings:
    return Settings(
        version="0.9.3",
        tick_interval_ms=16,
        process_name="DeadByDaylight-Win64-Shipping.exe",
        render=RenderSettings(show_killer=show_killer, max_distance_m=max_dist),
        hotkeys={},
    )


def test_survivor_in_range_is_rendered():
    fmt = EspFormatter(_settings())
    actors = [Actor(index=0, position=(1.0, 0.0, 5.0), role=ActorRole.SURVIVOR)]
    frame = fmt.format(actors, origin=(0.0, 0.0, 0.0))
    assert len(frame.entries) == 1
    assert frame.entries[0].role == "survivor"
    assert frame.entries[0].distance_m == 5.1


def test_killer_hidden_when_disabled():
    fmt = EspFormatter(_settings(show_killer=False))
    actors = [Actor(index=1, position=(2.0, 0.0, 3.0), role=ActorRole.KILLER)]
    frame = fmt.format(actors)
    assert frame.entries == []


def test_out_of_range_is_dropped():
    fmt = EspFormatter(_settings(max_dist=10.0))
    actors = [Actor(index=2, position=(100.0, 0.0, 0.0), role=ActorRole.SURVIVOR)]
    assert fmt.format(actors).entries == []