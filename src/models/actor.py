"""Actor entity model."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ActorRole(str, Enum):
    SURVIVOR = "survivor"
    KILLER = "killer"
    UNKNOWN = "unknown"


@dataclass
class Actor:
    index: int
    position: tuple[float, float, float]
    role: ActorRole
    health: float = 100.0

    @property
    def is_killer(self) -> bool:
        return self.role == ActorRole.KILLER