from PySide6.QtWidgets import QWidget

from bus.global_signal import global_signal
from config.__meta__ import Meta
from config.setting import setting
from theme.icon import icon
from theme.util import get_theme_icon
from ui.main_window.main_window import Ui_MainWindow
from widget.setting.setting import Setting


class MainWindow(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.reIcon()

        self.setWindowTitle(Meta.name)
        self.resize(setting.main_window_loc.w, setting.main_window_loc.h)
        self.move(setting.main_window_loc.x, setting.main_window_loc.y)

        setting_page = Setting(self)
        self.stacked_widget.addWidget(setting_page)

        global_signal.register_theme_changed_fn(self.reIcon)

    def closeEvent(self, event, /):
        setting.main_window_loc.x = self.x()
        setting.main_window_loc.y = self.y()
        setting.main_window_loc.w = self.width()
        setting.main_window_loc.h = self.height()
        setting.save()

        super().closeEvent(event)

    def reIcon(self):
        self.setWindowIcon(get_theme_icon(icon.code_assistant_protocol))
