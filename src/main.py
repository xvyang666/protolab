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


def main():
    import sys
    from PySide6 import QtAsyncio
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    from config.setting import setting
    from widget.main_window.main_window import MainWindow
    from config.path_config import PathConfig
    from bus.global_signal import global_signal
    from bus.global_ref import GlobalRef
    from theme.theme_mode import ThemeMode

    PathConfig.init_create_dir()
    setting.load()

    app = QApplication(sys.argv)
    app.setStyle(setting.style)
    GlobalRef.app = app

    _map: dict[ThemeMode, Qt.ColorScheme] = {
        ThemeMode.light: Qt.ColorScheme.Light,
        ThemeMode.dark: Qt.ColorScheme.Dark,
    }
    app.styleHints().setColorScheme(_map[setting.theme_mode])
    global_signal.register_changed_fn(theme_changed_fn=lambda t: app.styleHints().setColorScheme(_map[t]), )

    window = MainWindow()
    GlobalRef.main_window = window
    window.show()

    QtAsyncio.run()


if __name__ == "__main__":
    _err_handle()
    main()
