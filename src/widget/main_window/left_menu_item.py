from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

from bus.global_signal import global_signal
from theme.icon import IconEnum
from bus.obj import theme


class LeftMenuItem(QWidget):
    _is_selected_key = 'selected'

    def __init__(self, parent: QWidget, title: str, icon: IconEnum) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)  # 加这个才能用 qss 控制背景

        self.title = title
        self.icon = icon

        self._is_selected = False
        self.setProperty(self._is_selected_key, False)

        self.ar = QLabel(self)
        self.icon_label = QLabel(self)
        self.title_label = QLabel(self)

        layout = QHBoxLayout()
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        self.setLayout(layout)

        self.retranslateUi()
        self.rethemeUi()
        global_signal.register_changed_fn(theme_changed_fn=self.rethemeUi, language_changed_fn=self.retranslateUi)

    def mousePressEvent(self, event, /):
        self.set_selected(True)

    def set_selected(self, selected: bool) -> None:
        if self._is_selected == selected:
            return

        self._is_selected = selected
        self.setProperty(self._is_selected_key, selected)

        self.style().polish(self)  # 改完属性后腰重新应用 qss 生效

    def retranslateUi(self):
        self.title_label.setText(self.tr(self.title))

    def rethemeUi(self):
        self.icon_label.setPixmap(theme.get_icon(self.icon).pixmap(24, 24))

        c = theme.color
        self.setStyleSheet(f"""
            {self.__class__.__name__}[{self._is_selected_key}="true"] {{
                background-color: {c.action.selected};
                border-left: 2px solid {c.primary.main};
            }}
            
            {self.__class__.__name__}:hover {{
                background-color: {c.action.hover};
            }}
        """)
