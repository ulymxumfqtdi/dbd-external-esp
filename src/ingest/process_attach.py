"""Locate and attach to the Dead by Daylight game process."""
from __future__ import annotations

import time
from typing import Optional

import pymem
import pymem.process

from src.config.settings import Settings
from src.utils.logging_util import get_logger

log = get_logger("ingest.attach")


class ProcessAttachHandler:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.pm: Optional[pymem.Pymem] = None
        self.base_address: int = 0

    def attach(self) -> bool:
        deadline = time.time() + (self.settings.tick_interval_ms * 300 / 1000.0)
        while time.time() < deadline:
            try:
                self.pm = pymem.Pymem(self.settings.process_name)
                module = pymem.process.module_from_name(
                    self.pm.process_handle, self.settings.process_name
                )
                if module is None:
                    log.warning("game module not found, retrying")
                    time.sleep(0.25)
                    continue
                self.base_address = module.lpBaseOfDll
                log.info("attached to %s @ 0x%X", self.settings.process_name, self.base_address)
                return True
            except pymem.exception.ProcessNotFound:
                time.sleep(0.25)
        return False

    def detach(self) -> None:
        if self.pm is not None:
            try:
                self.pm.close_process()
            finally:
                self.pm = None
                self.base_address = 0

    @property
    def is_attached(self) -> bool:
        return self.pm is not None and self.base_address != 0