"""Format resolved actors into ESP frames for a driver."""
from __future__ import annotations

from dataclasses import dataclass, field

from src.config.settings import Settings
from src.models.actor import Actor, ActorRole
from src.utils.math_util import vec3_distance


@dataclass
class EspEntry:
    label: str
    role: str
    screen_hint: tuple[float, float]
    distance_m: float
    health: float


@dataclass
class EspFrame:
    entries: list[EspEntry] = field(default_factory=list)
    local_origin: tuple[float, float, float] = (0.0, 0.0, 0.0)


class EspFormatter:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def format(self, actors: list[Actor], origin: tuple[float, float, float] | None = None) -> EspFrame:
        origin = origin or (0.0, 0.0, 0.0)
        frame = EspFrame(local_origin=origin)
        for a in actors:
            if a.role == ActorRole.KILLER and not self.settings.render.show_killer:
                continue
            dist = vec3_distance(a.position, origin)
            if dist > self.settings.render.max_distance_m:
                continue
            frame.entries.append(
                EspEntry(
                    label=f"{a.role.value}#{a.index}",
                    role=a.role.value,
                    screen_hint=(a.position[0], a.position[1]),
                    distance_m=round(dist, 2),
                    health=a.health,
                )
            )
        return frame