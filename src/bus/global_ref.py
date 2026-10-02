if None:
    from PySide6.QtWidgets import QApplication
    from widget.main_window.main_window import MainWindow
    from util.toast_notifier import ToastNotifier


class GlobalRef:
    app: 'QApplication'
    main_window: 'MainWindow'
    main_window_notifier: 'ToastNotifier'
