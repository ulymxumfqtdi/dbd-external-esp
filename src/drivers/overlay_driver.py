"""Pygame overlay driver — draws ESP boxes on a transparent borderless window."""
from __future__ import annotations

import pygame

from src.config.settings import Settings
from src.processors.esp_formatter import EspFrame
from src.utils.logging_util import get_logger

log = get_logger("drivers.overlay")


class OverlayDriver:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._running = False
        self._screen: pygame.Surface | None = None
        self._font: pygame.font.Font | None = None

    def start(self) -> None:
        pygame.init()
        pygame.display.set_caption("dbd-external-esp [educational]")
        self._screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        self._font = pygame.font.SysFont("consolas", 14)
        self._running = True

    def is_running(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
        return self._running

    def render(self, frame: EspFrame) -> None:
        if self._screen is None or self._font is None:
            return
        self._screen.fill((0, 0, 0))
        for e in frame.entries:
            color = self.settings.render.box_color if e.role == "survivor" else (255, 60, 60)
            sx = int(960 + e.screen_hint[0] * 8)
            sy = int(540 - e.screen_hint[1] * 8)
            pygame.draw.rect(self._screen, color, (sx - 20, sy - 40, 40, 80), 2)
            text = f"{e.label} {e.distance_m:.0f}m"
            surf = self._font.render(text, True, self.settings.render.text_color)
            self._screen.blit(surf, (sx + 24, sy - 8))
        pygame.display.flip()

    def stop(self) -> None:
        self._running = False
        pygame.quit()