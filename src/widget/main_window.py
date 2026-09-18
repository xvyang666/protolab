from PySide6.QtWidgets import QWidget

from config.setting import setting


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('protolab')
        self.resize(setting.main_window_loc.w, setting.main_window_loc.h)
        self.move(setting.main_window_loc.x, setting.main_window_loc.y)

    def closeEvent(self, event, /):
        setting.main_window_loc.x = self.x()
        setting.main_window_loc.y = self.y()
        setting.main_window_loc.w = self.width()
        setting.main_window_loc.h = self.height()
        setting.save()

        super().closeEvent(event)