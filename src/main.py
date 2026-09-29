def _err_handle():
    """ 记录错误信息, 在所有语句前调用 """
    import sys
    import traceback
    import datetime
    from types import TracebackType

    def excepthook(e_type: type[BaseException], e_value: BaseException, tb: TracebackType | None):
        msg = ''.join(traceback.format_exception(e_type, e_value, tb))
        print(msg)

        t = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with open('crash.txt', 'a') as crash_f:
            crash_f.write(f'{t} {'-' * 32}\n{msg}')

    sys.excepthook = excepthook

    if '--debug' in sys.argv:
        debug_f = open('debug.txt', 'a')
        sys.stdout = debug_f
        sys.stderr = debug_f


async def main():
    from PySide6.QtCore import Qt
    from config.setting import setting
    from widget.main_window.main_window import MainWindow
    from config.path_config import PathConfig
    from bus.global_ref import GlobalRef
    from theme.theme_mode import ThemeMode

    PathConfig.init_create_dir()
    setting.load()

    app.setStyle(setting.style)

    _map: dict[ThemeMode, Qt.ColorScheme] = {
        ThemeMode.light: Qt.ColorScheme.Light,
        ThemeMode.dark: Qt.ColorScheme.Dark,
    }
    app.styleHints().setColorScheme(_map[setting.theme_mode])

    window = MainWindow()
    GlobalRef.main_window = window
    window.show()


if __name__ == "__main__":
    _err_handle()

    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6 import QtAsyncio
    from bus.global_ref import GlobalRef

    app = QApplication(sys.argv)
    GlobalRef.app = app

    QtAsyncio.run(main())
