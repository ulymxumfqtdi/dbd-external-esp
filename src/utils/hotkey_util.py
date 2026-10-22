"""Global hotkey wiring for toggles / panic key."""
from __future__ import annotations

from typing import Callable

try:
    import keyboard
except Exception:  # noqa: BLE001
    keyboard = None  # type: ignore[assignment]


class HotkeyManager:
    def __init__(self) -> None:
        self._bound: list[str] = []

    def bind(self, combo: str, callback: Callable[[], None]) -> None:
        if keyboard is None:
            return
        keyboard.add_hotkey(combo, callback, suppress=False)
        self._bound.append(combo)

    def bind_panic(self, combo: str, on_panic: Callable[[], None]) -> None:
        self.bind(combo, on_panic)

    def unbind_all(self) -> None:
        if keyboard is None:
            return
        for combo in self._bound:
            try:
                keyboard.remove_hotkey(combo)
            except Exception:  # noqa: BLE001
                pass
        self._bound.clear()