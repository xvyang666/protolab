if None:
    from PySide6.QtWidgets import QApplication
    from widget.main_window.main_window import MainWindow


class GlobalRef:
    app: 'QApplication'
    main_window: 'MainWindow'
