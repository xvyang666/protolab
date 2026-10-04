from typing import cast

from PySide6.QtCore import Qt, QRectF, QPersistentModelIndex, QModelIndex
from PySide6.QtGui import QPalette, QFont, QFontMetrics, QPainter, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle

from bus.obj import theme
from dev.test.hex_data_view.hex_view_model import HexViewModel, HexViewDirection


class HexViewDelegate(QStyledItemDelegate):
    Direction_To_Color = {
        HexViewDirection.TX: QColor(theme.color.primary.light),
        HexViewDirection.RX: QColor(theme.color.secondary.light),
    }
    assert len(Direction_To_Color) == len(HexViewDirection)

    def paint(self, painter, option, index):
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        col = index.column()
        if col == HexViewModel.Col_Index_Time:
            self.paint_date_time(painter, opt, index)
            return

        elif col == HexViewModel.Col_Index_Direction:
            self.paint_direction(painter, opt, index)
            return

        super().paint(painter, opt, index)

    def paint_direction(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex):
        model = cast(HexViewModel, index.model())
        row_data = model.get_row_data(index.row())

        # 创建 option 的副本，避免直接修改传入的原始 option 对象
        opt = QStyleOptionViewItem(option)

        if not (opt.state & QStyle.StateFlag.State_Selected):
            color = self.Direction_To_Color[row_data.direction]
            opt.palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, color)
            opt.palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, color)

        super().paint(painter, opt, index)

    def paint_date_time(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex):
        model = cast(HexViewModel, index.model())
        row_data = model.get_row_data(index.row())
        dt = row_data.date_time

        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        painter.save()

        # 1. 绘制默认背景 (包括选中时的高亮背景色)
        style = opt.widget.style() if opt.widget else QStyle()
        style.drawPrimitive(QStyle.PrimitiveElement.PE_PanelItemViewRow, opt, painter, opt.widget)

        # 2. 根据当前 opt.state (如是否 selected) 获取正确的文本颜色并设置给 painter
        if opt.state & QStyle.StateFlag.State_Selected:
            text_color = opt.palette.color(opt.palette.currentColorGroup(),QPalette.ColorRole.HighlightedText)
        else:
            text_color = opt.palette.color(opt.palette.currentColorGroup(),QPalette.ColorRole.Text)
        painter.setPen(text_color)

        local_dt = dt.astimezone()
        main_str = local_dt.strftime("%Y/%m/%d %H:%M:%S.")
        ms_str = f"{local_dt.microsecond // 1000:03d}"

        base_font = opt.font
        ms_font = QFont(base_font)
        ms_font.setPointSizeF(max(base_font.pointSizeF() - 2.5, 6.0))

        fm_main = QFontMetrics(base_font)
        fm_ms = QFontMetrics(ms_font)

        w_main = fm_main.horizontalAdvance(main_str)
        w_ms = fm_ms.horizontalAdvance(ms_str)

        padding = 4
        rect = opt.rect
        avail_width = rect.width() - (padding * 2)

        if avail_width > 0:
            painter.setClipRect(rect)

            x = rect.left() + padding

            if w_main + w_ms > avail_width:
                full_str = main_str + ms_str
                elided_str = fm_main.elidedText(
                    full_str, Qt.TextElideMode.ElideRight, avail_width
                )

                painter.setFont(base_font)
                painter.drawText(
                    QRectF(x, rect.top(), avail_width, rect.height()),
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                    elided_str,
                )
            else:
                # 计算主字体在当前 cell 居中时的基线 Y 坐标
                baseline_y = rect.top() + (rect.height() - fm_main.height()) / 2 + fm_main.ascent()

                # 绘制主时间 (基于 Baseline)
                painter.setFont(base_font)
                painter.drawText(int(x), int(baseline_y), main_str)

                # 绘制毫秒 (基于相同的 Baseline)
                painter.setFont(ms_font)
                painter.drawText(int(x + w_main), int(baseline_y), ms_str)

        painter.restore()