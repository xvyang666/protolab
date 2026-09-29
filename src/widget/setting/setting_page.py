from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QStyleFactory, QDialog

from bus.global_ref import GlobalRef
from bus.obj import theme
from config.setting import setting
from theme.icon import Icon
from theme.theme_mode import ThemeMode
from ui.setting.setting import Ui_Setting


class SettingPage(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ui = Ui_Setting()
        self.ui.setupUi(self)
        self.ui.style_icon.setPixmap(theme.get_icon(Icon.palette).pixmap(24, 24))
        self.ui.theme_icon.setPixmap(theme.get_icon(Icon.system_theme_selected).pixmap(24, 24))

        self.setWindowTitle(self.tr('设置'))

        for i in QStyleFactory.keys():
            self.ui.style_select.addItem(i, i)

        for i in ThemeMode:
            self.ui.theme_select.addItem(i.name, i)

        (index := self.ui.style_select.findData(setting.style)) != -1 and self.ui.style_select.setCurrentIndex(index)
        (index := self.ui.theme_select.findData(setting.theme_mode)) != -1 and self.ui.theme_select.setCurrentIndex(index)

        self.ui.style_select.currentIndexChanged.connect(self.style_changed)
        self.ui.theme_select.currentIndexChanged.connect(self.theme_changed)

    def style_changed(self, _index: int):
        style: str = self.ui.style_select.currentData(Qt.ItemDataRole.UserRole)
        setting.style = style
        GlobalRef.app.setStyle(style)

    def theme_changed(self, _index: int):
        mode: ThemeMode = self.ui.theme_select.currentData(Qt.ItemDataRole.UserRole)
        setting.theme_mode = mode
