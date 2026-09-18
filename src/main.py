def _err_handle():
    """ 记录错误信息, 在所有语句前调用 """
    import sys
    import traceback
    import datetime
    from types import TracebackType

    def excepthook(e_type: type[BaseException], e_value: BaseException, tb: TracebackType | None):
        with open('crash.txt', 'a') as crash_f:
            t = datetime.datetime.now(datetime.timezone.utc).isoformat()
            msg = ''.join(traceback.format_exception(e_type, e_value, tb))
            crash_f.write(f'{t} {'-' * 32}\n{msg}')

    sys.excepthook = excepthook

    if '--debug' in sys.argv:
        debug_f = open('debug.txt', 'a')
        sys.stdout = debug_f
        sys.stderr = debug_f


def main():
    _err_handle()

    import sys
    from PySide6 import QtAsyncio
    from PySide6.QtWidgets import QApplication
    from config.setting import setting
    from widget.main_window import MainWindow
    from config.path_config import PathConfig

    PathConfig.init()
    setting.load()

    app = QApplication(sys.argv)
    app.setStyle(setting.qt_style)

    window = MainWindow()
    window.show()

    QtAsyncio.run()


if __name__ == "__main__":
    main()
