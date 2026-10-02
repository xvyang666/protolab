from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QStyleFactory, QDialog

from bus.global_ref import GlobalRef
from bus.obj import theme
from config.setting import setting
from theme.icon import Icon
from theme.theme_mode import ThemeMode
from ui.setting.setting_page import Ui_SettingPage
from util.combobox_set_default import combobox_set_default
from util.language_enum import LanguageEnum


class SettingPage(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ui = Ui_SettingPage()
        self.ui.setupUi(self)
        self.ui.style_icon.setPixmap(theme.get_icon(Icon.palette).pixmap(24, 24))
        self.ui.theme_icon.setPixmap(theme.get_icon(Icon.system_theme_selected).pixmap(24, 24))

        self.setWindowTitle(self.tr('设置'))

        for i in QStyleFactory.keys():
            self.ui.style_select.addItem(i, i)

        for i in ThemeMode:
            self.ui.theme_select.addItem(i.name, i)

        for i in LanguageEnum:
            self.ui.language_select.addItem(_language_name[i], i)

        combobox_set_default(self.ui.style_select, setting.style)
        combobox_set_default(self.ui.theme_select, setting.theme_mode)
        combobox_set_default(self.ui.language_select, setting.language)

        self.ui.style_select.currentIndexChanged.connect(self.style_changed)
        self.ui.theme_select.currentIndexChanged.connect(self.theme_changed)
        self.ui.language_select.currentIndexChanged.connect(self.language_changed)

    def style_changed(self, _index: int):
        style: str = self.ui.style_select.currentData(Qt.ItemDataRole.UserRole)
        setting.style = style
        GlobalRef.app.setStyle(style)

    def theme_changed(self, _index: int):
        mode: ThemeMode = self.ui.theme_select.currentData(Qt.ItemDataRole.UserRole)
        setting.theme_mode = mode

    def language_changed(self, _index: int):
        lan: LanguageEnum = self.ui.language_select.currentData(Qt.ItemDataRole.UserRole)
        setting.language = lan


_language_name: dict[LanguageEnum, str] = {
    LanguageEnum.en: 'English',
    LanguageEnum.zh_CN: '中文',
}
assert len(_language_name) == len(LanguageEnum)