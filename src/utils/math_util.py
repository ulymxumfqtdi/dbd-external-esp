"""Vector math helpers for world-space ESP calculations."""
from __future__ import annotations

import math

Vec3 = tuple[float, float, float]


def vec3_distance(a: Vec3, b: Vec3) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def vec3_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def world_to_screen(world: Vec3, fov: float = 90.0, aspect: float = 16 / 9) -> tuple[float, float]:
    """Cheap perspective projection — enough for a placeholder overlay."""
    x, y, z = world
    if z <= 0.1:
        return (0.0, 0.0)
    f = 1.0 / math.tan(math.radians(fov) / 2.0)
    sx = (x * f / aspect) / z
    sy = (y * f) / z
    return (sx, sy)