from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPlainTextEdit


class ReadOnlyTextEdit(QPlainTextEdit):
    """
    可显示闪烁光标、拦截任何修改并弹出 ToolTip 提示的 QTextEdit
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByKeyboard |
            Qt.TextInteractionFlag.TextSelectableByMouse  # type: ignore
        )
