"""Resolve version-specific offsets. Placeholder values only."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Offsets:
    gworld: int
    local_player: int
    entity_list: int
    entity_count: int
    actor_location: int
    actor_health: int
    actor_is_killer: int
    actor_team: int


# NOTE: these are DUMMY offsets for pipeline research. Do not use in-game.
_PLACEHOLDER = Offsets(
    gworld=0x0,
    local_player=0x0,
    entity_list=0x0,
    entity_count=0x0,
    actor_location=0x0,
    actor_health=0x0,
    actor_is_killer=0x0,
    actor_team=0x0,
)


def resolve_offsets(version: str) -> Offsets:
    """Return offsets for a given game version. Always placeholders in this repo."""
    return _PLACEHOLDER