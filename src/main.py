def err_handle():
    """ 记录错误信息, 在所有语句前调用 """
    import sys
    import traceback
    import datetime
    from types import TracebackType

    def excepthook(e_type: type[BaseException], e_value: BaseException, tb: TracebackType | None):
        with open('crash.txt', 'a') as f:
            t = datetime.datetime.now(datetime.timezone.utc).isoformat()
            msg = ''.join(traceback.format_exception(e_type, e_value, tb))
            f.write(f'{t} {'-' * 32}\n{msg}')

    sys.excepthook = excepthook

    if '--debug' in sys.argv:
        f = open('debug.txt', 'a')
        sys.stdout = f
        sys.stderr = f


def open_window():
    """ 启动窗口 """
    import sys
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6 import QtAsyncio

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = QWidget()
    window.show()

    QtAsyncio.run()


def main():
    err_handle()
    open_window()


if __name__ == "__main__":
    main()
