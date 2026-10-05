from enum import Enum

from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QParallelAnimationGroup, QPoint, QEvent,
    QObject, Signal, QSize
)
from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QPushButton, QFrame, QVBoxLayout, QGraphicsOpacityEffect
)

from bus.obj import theme
from theme.color import ColorVariant
from theme.icon import IconEnum, Icon


class Level(Enum):
    info = "info"
    warning = "warning"
    error = "error"
    success = "success"


color_map: dict[Level, ColorVariant] = {
    Level.info: theme.color.info,
    Level.warning: theme.color.warning,
    Level.error: theme.color.error,
    Level.success: theme.color.success,
}

assert len(color_map) == len(Level)

icon_map: dict[Level, IconEnum] = {
    Level.info: Icon.information_dialog,
    Level.warning: Icon.warning_dialog,
    Level.error: Icon.error_dialog,
    Level.success: Icon.success_dialog,
}

assert len(icon_map) == len(Level)


class _ToastItem(QFrame):
    closed = Signal(object)

    def __init__(
            self,
            parent: QWidget,
            text: str,
            level: Level,
            duration: int = 5000,
    ):
        super().__init__(parent)
        self.text = text
        self.level = level
        self.duration = duration

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_close)
        self.timer.setInterval(self.duration)
        self.timer.start()

        self._is_closing = False

        self._init_ui()

    def _init_ui(self):
        # 不同等级的颜色配置
        c = color_map[self.level]
        self.setStyleSheet(
            f"""{self.__class__.__name__} {{
                background-color: {theme.color.background.default};
                border: 1px solid {c.main};
                border-radius: 6px;
            }}
            QLabel {{
                color: {c.main};
                font-size: 12px;
            }}"""
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 10, 8)
        layout.setSpacing(10)

        # 图标
        icon_layout = QVBoxLayout()
        icon_label = QLabel(self)
        icon_label.setPixmap(theme.get_icon(icon_map[self.level]).pixmap(16, 16))
        icon_layout.addWidget(icon_label)
        icon_layout.addStretch()
        layout.addLayout(icon_layout)

        # 文本
        msg_label = QLabel(self.text, self)
        msg_label.setWordWrap(True)
        msg_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(msg_label)

        # 关闭按钮
        btn_layout = QVBoxLayout()
        close_btn = QPushButton(self)
        close_btn.setFlat(True)
        close_btn.setIcon(theme.get_icon(Icon.close))
        close_btn.setIconSize(QSize(16, 16))
        close_btn.setFixedSize(18, 18)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.start_close)
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.adjustSize()

    def start_close(self):
        if self._is_closing:
            return
        self._is_closing = True
        self.closed.emit(self)

    def enterEvent(self, event, /):
        self.timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event, /):
        self.timer.start()
        super().leaveEvent(event)


class ToastNotifier(QObject):
    """TopLevel 界面浮动提示通知管理器"""

    class VPos(Enum):
        top = "top"
        center = "center"
        bottom = "bottom"

    class HPos(Enum):
        left = "left"
        center = "center"
        right = "right"

    def __init__(
            self,
            parent: QWidget,
            v_pos: VPos = VPos.top,
            h_pos: HPos = HPos.right,
            max_count: int = 5,
            duration: int = 5000,
            anim_duration: int = 200
    ):
        super().__init__(parent)
        self.parent_widget = parent
        self.v_pos = v_pos
        self.h_pos = h_pos
        self.max_count = max_count
        self.duration = duration
        self.anim_duration = anim_duration

        self.toasts: list[_ToastItem] = []

        self.parent_widget.installEventFilter(self)  # 监听父组件 Resize 事件以自动调整布局位置

    def show(self, text: str, level: Level = Level.info):
        """显示一条 Toast 提示"""
        # 超出最大数量时直接关掉最早的一条
        if len(self.toasts) >= self.max_count:
            oldest = self.toasts[0]
            self._close_toast(oldest, immediate=True)

        toast = _ToastItem(
            parent=self.parent_widget,
            text=text,
            level=level,
            duration=self.duration,
        )
        toast.closed.connect(self._on_toast_closed)
        self.toasts.append(toast)

        toast.show()
        self._reposition_toasts(animate_target=toast)

    def info(self, text: str):
        self.show(text, Level.info)

    def warning(self, text: str):
        self.show(text, Level.warning)

    def error(self, text: str):
        self.show(text, Level.error)

    def success(self, text: str):
        self.show(text, Level.success)

    def _on_toast_closed(self, toast: _ToastItem):
        self._close_toast(toast)

    def _close_toast(self, toast: _ToastItem, immediate: bool = False):
        if toast not in self.toasts:
            return

        self.toasts.remove(toast)

        if immediate:
            toast.deleteLater()
            self._reposition_toasts()
            return

        # 退出动画: 淡出 + 位置滑动
        anim_group = QParallelAnimationGroup(self)

        pos_anim = QPropertyAnimation(toast, b"pos", anim_group)
        pos_anim.setDuration(self.anim_duration)
        pos_anim.setStartValue(toast.pos())

        offset_y = -32 if self.v_pos == self.VPos.top else 32
        pos_anim.setEndValue(QPoint(toast.x(), toast.y() + offset_y))
        anim_group.addAnimation(pos_anim)

        opacity_anim = QPropertyAnimation(toast.opacity_effect, b"opacity", anim_group)
        opacity_anim.setDuration(self.anim_duration)
        opacity_anim.setStartValue(toast.opacity_effect.opacity())
        opacity_anim.setEndValue(0.0)
        anim_group.addAnimation(opacity_anim)

        def on_finished():
            toast.deleteLater()
            self._reposition_toasts()

        anim_group.finished.connect(on_finished)
        anim_group.start()

    def _reposition_toasts(self, animate_target: _ToastItem | None = None, animated: bool = True):
        """重新计算并平滑移动所有 Toast 的坐标位置"""
        if not self.toasts:
            return

        pw = self.parent_widget.width()
        ph = self.parent_widget.height()
        margin_x, margin_y, spacing = 20, 20, 10

        # 计算垂直方向起点与堆叠顺序
        if self.v_pos == self.VPos.top:
            curr_y = margin_y
        elif self.v_pos == self.VPos.bottom:
            total_h = sum(t.height() for t in self.toasts) + (len(self.toasts) - 1) * spacing
            curr_y = ph - margin_y - total_h
        elif self.v_pos == self.VPos.center:
            total_h = sum(t.height() for t in self.toasts) + (len(self.toasts) - 1) * spacing
            curr_y = (ph - total_h) // 2
        else:
            raise ValueError

        for toast in self.toasts:
            # 计算水平坐标
            if self.h_pos == self.HPos.left:
                target_x = margin_x
            elif self.h_pos == self.HPos.right:
                target_x = pw - margin_x - toast.width()
            elif self.h_pos == self.HPos.center:
                target_x = (pw - toast.width()) // 2
            else:
                raise ValueError

            target_y = curr_y
            curr_y += toast.height() + spacing
            target_pos = QPoint(target_x, target_y)

            if not animated:
                toast.move(target_pos)
                toast.opacity_effect.setOpacity(1.0)

            else:
                # 如果是刚创建的新 Item, 则播放淡入+滑动进场动画
                if toast == animate_target:
                    slide_offset = -15 if self.v_pos == self.VPos.top else 15
                    start_pos = QPoint(target_x, target_y + slide_offset)

                    anim_group = QParallelAnimationGroup(self)

                    pos_anim = QPropertyAnimation(toast, b"pos", anim_group)
                    pos_anim.setDuration(self.anim_duration)
                    pos_anim.setStartValue(start_pos)
                    pos_anim.setEndValue(target_pos)
                    anim_group.addAnimation(pos_anim)

                    opacity_anim = QPropertyAnimation(toast.opacity_effect, b"opacity", anim_group)
                    opacity_anim.setDuration(self.anim_duration)
                    opacity_anim.setStartValue(0.0)
                    opacity_anim.setEndValue(1.0)
                    anim_group.addAnimation(opacity_anim)

                    anim_group.start()
                else:
                    # 现有 Item 平滑滑动到新槽位
                    pos_anim = QPropertyAnimation(toast, b"pos", self)
                    pos_anim.setDuration(self.anim_duration)
                    pos_anim.setStartValue(toast.pos())
                    pos_anim.setEndValue(target_pos)
                    pos_anim.start()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.parent_widget and event.type() == QEvent.Type.Resize:
            self._reposition_toasts(animated=False)
        return super().eventFilter(watched, event)
