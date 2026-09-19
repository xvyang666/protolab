from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QStyleFactory

from bus.global_ref import GlobalRef
from config.setting import setting
from theme.icon import get_theme_icon
from theme.themeMode import ThemeMode
from ui.setting.setting import Ui_Setting


class Setting(QWidget, Ui_Setting):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setupUi(self)
        self.reIcon()

        for i in QStyleFactory.keys():
            self.style_select.addItem(i, i)

        for i in ThemeMode:
            self.theme_select.addItem(i.name, i)

        (index := self.style_select.findData(setting.qt_style)) != -1 and self.style_select.setCurrentIndex(index)
        (index := self.theme_select.findData(setting.theme)) != -1 and self.theme_select.setCurrentIndex(index)

        self.style_select.currentIndexChanged.connect()

    def style_changed(self, _index: int):
        style: str = self.style_select.currentData(Qt.ItemDataRole.UserRole)
        GlobalRef.app.setStyle(style)

    def reIcon(self):
        icon = get_theme_icon()
        self.style_icon.setPixmap(icon.code_assistant_protocol.pixmap(24, 24))
        self.theme_icon.setPixmap(icon.code_assistant_protocol.pixmap(24, 24))
