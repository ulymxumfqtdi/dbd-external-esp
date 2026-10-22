"""Entry point / bootstrap for the external ESP pipeline."""
from __future__ import annotations

import argparse
import sys
import time

from src.config.settings import load_settings
from src.ingest.process_attach import ProcessAttachHandler
from src.ingest.memory_reader import MemoryReaderHandler
from src.processors.entity_resolver import EntityResolver
from src.processors.esp_formatter import EspFormatter
from src.drivers.overlay_driver import OverlayDriver
from src.drivers.console_driver import ConsoleDriver
from src.utils.logging_util import get_logger

log = get_logger("main")


def build_pipeline(settings):
    attach = ProcessAttachHandler(settings)
    reader = MemoryReaderHandler(settings, attach)
    resolver = EntityResolver(settings, reader)
    formatter = EspFormatter(settings)
    return attach, reader, resolver, formatter


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dbd-external-esp")
    parser.add_argument("--dry-run", action="store_true", help="skip memory reads")
    parser.add_argument("--driver", choices=["overlay", "console"], default="console")
    parser.add_argument("--config", default="config/default.toml")
    args = parser.parse_args(argv)

    settings = load_settings(args.config)
    log.info("starting dbd-external-esp v%s (driver=%s)", settings.version, args.driver)

    attach, reader, resolver, formatter = build_pipeline(settings)

    if not args.dry_run and not attach.attach():
        log.error("failed to attach to DeadByDaylight-Win64-Shipping.exe")
        return 1

    driver = OverlayDriver(settings) if args.driver == "overlay" else ConsoleDriver(settings)
    driver.start()

    try:
        while driver.is_running():
            snapshot = reader.read_snapshot()
            entities = resolver.resolve(snapshot)
            frame = formatter.format(entities)
            driver.render(frame)
            time.sleep(settings.tick_interval_ms / 1000.0)
    except KeyboardInterrupt:
        log.info("interrupted by user")
    finally:
        driver.stop()
        attach.detach()
    return 0


if __name__ == "__main__":
    sys.exit(main())