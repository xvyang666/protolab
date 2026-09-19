from typing import Callable

from PySide6.QtCore import QObject, Signal

from theme.themeMode import ThemeMode


class _GlobalSignal(QObject):
    theme_changed = Signal(ThemeMode)

    def register_theme_changed_fn(self, fn: Callable[[ThemeMode], None] | Callable[[], None]):
        self.theme_changed.connect(fn)


global_signal: _GlobalSignal = _GlobalSignal()
