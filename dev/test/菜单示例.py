import sys
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QStyle,
    QWidget,
)

class Win11Sidebar(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self.setIconSize(QSize(18, 18))
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Win11 Fluent Design 暗色主题样式
        self.setStyleSheet("""
            QListWidget {
                background-color: #202020;
                border: none;
                outline: none;
                padding: 6px;
            }
            QListWidget::item {
                height: 36px;
                padding-left: 12px;
                border-radius: 5px;
                color: #d1d1d1;
                font-family: "Segoe UI", "Microsoft YaHei";
                font-size: 13px;
            }
            QListWidget::item:hover {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #383838;
                color: #ffffff;
            }
        """)

        # 蓝色的指示条 (Pill Indicator)
        self.indicator = QWidget(self)
        self.indicator.setStyleSheet("background-color: #60cdff; border-radius: 1.5px;")
        self.indicator.resize(3, 16)
        self.indicator.hide()

        # 动画配置
        self.anim = QPropertyAnimation(self.indicator, b"geometry")
        self.anim.setDuration(220)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # 信号连接
        self.currentItemChanged.connect(self._on_item_changed)
        # 列表滚动时保持指示条在当前选中的 Item 对应位置
        self.verticalScrollBar().valueChanged.connect(self._sync_indicator_position)

    def _get_target_rect(self, item: QListWidgetItem) -> QRect:
        item_rect = self.visualItemRect(item)
        pill_w, pill_h = 3, 16
        # 相对于 Item 内部居左且垂直居中
        target_x = item_rect.x() + 3
        target_y = item_rect.y() + (item_rect.height() - pill_h) // 2
        return QRect(target_x, target_y, pill_w, pill_h)

    def _on_item_changed(self, current: QListWidgetItem, previous: QListWidgetItem):
        if not current:
            self.indicator.hide()
            return

        target_rect = self._get_target_rect(current)

        if not self.indicator.isVisible():
            self.indicator.setGeometry(target_rect)
            self.indicator.show()
            self.indicator.raise_()  # 保证指示条置于顶层
            return

        self.anim.stop()
        self.anim.setStartValue(self.indicator.geometry())
        self.anim.setEndValue(target_rect)
        self.anim.start()

    def _sync_indicator_position(self):
        current = self.currentItem()
        if current and self.indicator.isVisible():
            self.indicator.setGeometry(self._get_target_rect(current))

    def add_menu_item(self, text: str, icon: QIcon):
        item = QListWidgetItem(icon, text)
        self.addItem(item)
        return item

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle('fusion')
    w = Win11Sidebar()

    # 1. 使用系统内置图标作为示例 (实际项目替换为 QIcon("path/to/icon.svg"))
    style = app.style()
    items_data = [
        ("Home", style.standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon)),
        ("Documents", style.standardIcon(QStyle.StandardPixmap.SP_DirIcon)),
        ("Downloads", style.standardIcon(QStyle.StandardPixmap.SP_ArrowDown)),
        ("Pictures", style.standardIcon(QStyle.StandardPixmap.SP_FileIcon)),
        # ("Settings", style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailView)),
    ]

    for text, icon in items_data:
        w.add_menu_item(text, icon)

    # 默认选中第一项
    w.setCurrentRow(0)

    w.show()
    sys.exit(app.exec())