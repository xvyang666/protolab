import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

# 待测试的颜色格式列表
COLOR_TEST_CASES = [
    ("颜色名称 (red)", "red"),
    ("颜色名称 (transparent)", "transparent"),
    ("短十六进制 (#f00)", "#f00"),
    ("标准十六进制 (#ff0000)", "#ff0000"),
    ("Qt Hex ARGB (#80ff0000)", "#80ff0000"),
    ("CSS Hex RGBA (#ff000080)", "#ff000080"),
    ("RGB 整数 (rgb(255, 0, 0))", "rgb(255, 0, 0)"),
    ("RGB 百分比 (rgb(100%, 0%, 0%))", "rgb(100%, 0%, 0%)"),
    ("RGBA 整数 Alpha (rgba(255, 0, 0, 128))", "rgba(255, 0, 0, 128)"),
    ("RGBA 浮点 Alpha (rgba(255, 0, 0, 0.5))", "rgba(255, 0, 0, 0.5)"),
    ("HSV 格式 (hsv(0, 255, 255))", "hsv(0, 255, 255)"),
    ("HSVA 格式 (hsva(0, 255, 255, 128))", "hsva(0, 255, 255, 128)"),
    ("HSL 格式 (hsl(0, 100%, 50%))", "hsl(0, 100%, 50%)"),
]


class ColorCompareTestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSS vs QColor 颜色格式解析对比测试")
        self.resize(750, 600)

        main_layout = QVBoxLayout(self)

        # 提示语
        tip_label = QLabel(
            "说明: 左侧使用 QSS (setStyleSheet) 解析, 右侧使用 QColor 原生构造及 QPalette 渲染.\n"
            "若 QColor 解析失败 (isValid == False), 右侧将显式标记红框警告."
        )
        tip_label.setStyleSheet("color: #aaa; font-size: 12px; margin-bottom: 8px;")
        main_layout.addWidget(tip_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        for idx, (title, color_val) in enumerate(COLOR_TEST_CASES):
            box = QGroupBox()
            box_layout = QHBoxLayout(box)

            # 1. 左侧: QSS 解析测试块
            qss_label = QLabel(f"background-color: {color_val}")
            qss_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qss_label.setFixedHeight(50)
            qss_label.setStyleSheet(
                f"background-color: {color_val}"
            )

            # 2. 右侧: QColor 原生解析测试块
            qcolor_label = QLabel(f"QColor({color_val})")
            qcolor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qcolor_label.setFixedHeight(50)

            qc = QColor(color_val)
            if qc.isValid():
                palette = qcolor_label.palette()
                palette.setColor(QPalette.ColorRole.Window, qc)
                qcolor_label.setPalette(palette)
                qcolor_label.setAutoFillBackground(True)
            else:
                qcolor_label.setText("QColor 解析失败")

            box_layout.addWidget(qss_label)
            box_layout.addWidget(qcolor_label)

            grid.addWidget(box, idx, 0)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorCompareTestWindow()
    window.show()
    sys.exit(app.exec())