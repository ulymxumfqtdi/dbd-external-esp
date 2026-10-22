"""Raw memory reader — pulls entity table snapshots from the game."""
from __future__ import annotations

from dataclasses import dataclass

from src.config.settings import Settings
from src.ingest.process_attach import ProcessAttachHandler
from src.offsets import resolve_offsets
from src.utils.logging_util import get_logger

log = get_logger("ingest.reader")


@dataclass
class RawSnapshot:
    tick: int
    local_player_ptr: int
    entity_list_ptr: int
    entity_count: int
    game_state: str


class MemoryReaderHandler:
    def __init__(self, settings: Settings, attach: ProcessAttachHandler) -> None:
        self.settings = settings
        self.attach = attach
        self.offsets = resolve_offsets(settings.version)
        self._tick = 0

    def read_snapshot(self) -> RawSnapshot:
        self._tick += 1
        if not self.attach.is_attached or self.attach.pm is None:
            return RawSnapshot(self._tick, 0, 0, 0, "detached")

        pm = self.attach.pm
        base = self.attach.base_address
        try:
            gworld = pm.read_longlong(base + self.offsets.gworld)
            local = pm.read_longlong(gworld + self.offsets.local_player)
            ent_list = pm.read_longlong(gworld + self.offsets.entity_list)
            count = pm.read_int(gworld + self.offsets.entity_count)
        except Exception as exc:  # noqa: BLE001
            log.debug("snapshot read failed: %s", exc)
            return RawSnapshot(self._tick, 0, 0, 0, "error")

        return RawSnapshot(self._tick, local, ent_list, count, "ingame")