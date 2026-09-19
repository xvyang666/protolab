from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QStyleFactory

from bus.global_ref import GlobalRef
from bus.global_signal import global_signal
from config.setting import setting
from theme.icon import icon
from theme.themeMode import ThemeMode
from theme.util import get_theme_icon
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

        (index := self.style_select.findData(setting.style)) != -1 and self.style_select.setCurrentIndex(index)
        (index := self.theme_select.findData(setting.theme)) != -1 and self.theme_select.setCurrentIndex(index)

        self.style_select.currentIndexChanged.connect(self.style_changed)
        self.theme_select.currentIndexChanged.connect(self.theme_changed)

        global_signal.theme_changed.connect(self.reIcon)

    def style_changed(self, _index: int):
        style: str = self.style_select.currentData(Qt.ItemDataRole.UserRole)
        setting.style = style
        GlobalRef.app.setStyle(style)

    def theme_changed(self, _index: int):
        theme: ThemeMode = self.theme_select.currentData(Qt.ItemDataRole.UserRole)
        setting.theme = theme
        global_signal.theme_changed.emit(theme)

    def reIcon(self):
        self.style_icon.setPixmap(get_theme_icon(icon.code_assistant_protocol).pixmap(24, 24))
        self.theme_icon.setPixmap(get_theme_icon(icon.code_assistant_protocol).pixmap(24, 24))
