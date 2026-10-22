"""Simple console output driver for dry-run / CI testing."""
from __future__ import annotations

import sys

from src.config.settings import Settings
from src.processors.esp_formatter import EspFrame
from src.utils.logging_util import get_logger

log = get_logger("drivers.console")


class ConsoleDriver:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._running = False

    def start(self) -> None:
        self._running = True
        log.info("console driver started")

    def is_running(self) -> bool:
        return self._running

    def render(self, frame: EspFrame) -> None:
        if not frame.entries:
            return
        for e in frame.entries:
            sys.stdout.write(
                f"[{e.role:8}] {e.label:14} dist={e.distance_m:6.2f}m hp={e.health:5.1f}\n"
            )
        sys.stdout.flush()

    def stop(self) -> None:
        self._running = False