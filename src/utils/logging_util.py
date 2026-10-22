"""Logging helper — colored console logger."""
from __future__ import annotations

import logging
import sys

try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init()
    _HAS_COLOR = True
except Exception:  # noqa: BLE001
    _HAS_COLOR = False


class _Formatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
    }

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if _HAS_COLOR:
            color = self.COLORS.get(record.levelno, "")
            return f"{color}{msg}\033[0m"
        return msg


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(f"dbd-esp.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.propagate = False
    return logger