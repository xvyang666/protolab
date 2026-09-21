from PySide6.QtWidgets import QWidget, QVBoxLayout

from bus.global_signal import global_signal
from config.__meta__ import Meta
from config.setting import setting
from theme.icon import Icon
from bus.obj import theme
from ui.main_window.main_window import Ui_MainWindow
from widget.main_window.left_menu_item import LeftMenuItem
from widget.setting.setting import Setting


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.rethemeUi()

        self.setWindowTitle(Meta.name)
        self.resize(setting.main_window_loc.w, setting.main_window_loc.h)
        self.move(setting.main_window_loc.x, setting.main_window_loc.y)

        left_menu_layout = self.ui.left_meun.layout().layout()
        assert isinstance(left_menu_layout, QVBoxLayout)
        setting_item = LeftMenuItem(self, title='设置', icon=Icon.settings)
        left_menu_layout.addStretch()
        left_menu_layout.addWidget(setting_item)

        setting_page = Setting(self)
        self.ui.stacked_widget.addWidget(setting_page)

        global_signal.register_changed_fn(theme_changed_fn=self.rethemeUi)

    def closeEvent(self, event, /):
        setting.main_window_loc.x = self.x()
        setting.main_window_loc.y = self.y()
        setting.main_window_loc.w = self.width()
        setting.main_window_loc.h = self.height()
        setting.save()

        super().closeEvent(event)

    def rethemeUi(self):
        self.setWindowIcon(theme.get_icon(Icon.code_assistant_protocol))
