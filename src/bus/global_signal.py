from typing import Callable

from PySide6.QtCore import QObject, Signal

from theme.theme_mode import ThemeMode


class _GlobalSignal(QObject):
    theme_changed = Signal(ThemeMode)
    languale_changed = Signal()  # todo 语言切换事件

    def register_changed_fn(
            self,
            *,
            theme_changed_fn: Callable[[ThemeMode], None] | Callable[[], None] | None = None,
            language_changed_fn: Callable[[], None] | None = None,
    ):
        if theme_changed_fn is not None:
            self.theme_changed.connect(theme_changed_fn)

        if language_changed_fn is not None:
            self.languale_changed.connect(language_changed_fn)


global_signal: _GlobalSignal = _GlobalSignal()
