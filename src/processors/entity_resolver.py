"""Resolve raw entity list pointers into typed actor entities."""
from __future__ import annotations

import math
from dataclasses import dataclass

from src.config.settings import Settings
from src.ingest.memory_reader import MemoryReaderHandler, RawSnapshot
from src.models.actor import Actor, ActorRole
from src.utils.math_util import vec3_distance
from src.utils.logging_util import get_logger

log = get_logger("processors.resolver")


class EntityResolver:
    def __init__(self, settings: Settings, reader: MemoryReaderHandler) -> None:
        self.settings = settings
        self.reader = reader
        self.offsets = reader.offsets

    def resolve(self, snap: RawSnapshot) -> list[Actor]:
        if snap.game_state != "ingame" or snap.entity_count == 0:
            return []
        pm = self.reader.attach.pm
        if pm is None:
            return []

        actors: list[Actor] = []
        for i in range(min(snap.entity_count, 64)):
            try:
                actor_ptr = pm.read_longlong(snap.entity_list_ptr + i * 0x8)
                if actor_ptr == 0:
                    continue
                loc = pm.read_bytes(actor_ptr + self.offsets.actor_location, 12)
                x, y, z = (
                    float.fromhex("0x" + loc[0:4][::-1].hex()),
                    float.fromhex("0x" + loc[4:8][::-1].hex()),
                    float.fromhex("0x" + loc[8:12][::-1].hex()),
                )
                is_killer = bool(pm.read_bytes(actor_ptr + self.offsets.actor_is_killer, 1)[0])
                health = pm.read_float(actor_ptr + self.offsets.actor_health)
            except Exception:  # noqa: BLE001
                continue

            actors.append(
                Actor(
                    index=i,
                    position=(x, y, z),
                    role=ActorRole.KILLER if is_killer else ActorRole.SURVIVOR,
                    health=health,
                )
            )
        return actors