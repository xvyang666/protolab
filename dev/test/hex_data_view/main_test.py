import sys
from datetime import datetime, timezone

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton
)

from dev.test.hex_data_view.hex_view_model import HexViewRowData, HexViewDirection
from dev.test.hex_data_view.hex_view_widget import HexViewWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_widget = QWidget()
    layout = QVBoxLayout(main_widget)

    hex_view = HexViewWidget()
    layout.addWidget(hex_view)

    btn_in = QPushButton("从外部添加 IN 数据")
    btn_out = QPushButton("从外部添加 OUT 数据")

    btn_in.clicked.connect(lambda: hex_view.append_row(HexViewRowData(datetime.now(timezone.utc), b"\x00\x20\x326\n66" * 5, HexViewDirection.RX)))
    btn_out.clicked.connect(lambda: hex_view.append_row(HexViewRowData(datetime.now(timezone.utc), b"A1 B2 C3", HexViewDirection.TX)))
    layout.addWidget(btn_in)
    layout.addWidget(btn_out)

    main_widget.resize(600, 500)
    main_widget.show()

    btn_in.click()

    sys.exit(app.exec())
