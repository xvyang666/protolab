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
    from util.toast_notifier import ToastNotifier
    from bus.obj import theme
    from util.language_enum import install_translator_helper

    PathConfig.init_create_dir()
    setting.load()
    theme.mode = setting.theme_mode

    GlobalRef.app.setStyle(setting.style)
    install_translator_helper(GlobalRef.app, setting.language)
    GlobalRef.app.styleHints().setColorScheme(
        {
            ThemeMode.light: Qt.ColorScheme.Light,
            ThemeMode.dark: Qt.ColorScheme.Dark,
        }[setting.theme_mode]
    )

    window = GlobalRef.main_window = MainWindow()
    window.show()

    GlobalRef.main_window_notifier = ToastNotifier(window)


if __name__ == "__main__":
    _err_handle()

    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6 import QtAsyncio
    from bus.global_ref import GlobalRef

    GlobalRef.app = QApplication(sys.argv)

    QtAsyncio.run(main())
