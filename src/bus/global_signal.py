from PySide6.QtCore import QObject


class _GlobalSignal(QObject):
    ...


global_signal: _GlobalSignal = _GlobalSignal()
