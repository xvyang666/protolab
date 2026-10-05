from typing import cast

from PySide6.QtCore import QPersistentModelIndex, QModelIndex, QObject
from PySide6.QtGui import QPalette, QPainter, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from comp.hex_data_view.model import HexViewModel
from comp.hex_data_view.types import HexViewDirection


class HexViewDelegate(QStyledItemDelegate):

    def __init__(self, parent: QObject | None = None, /, tx_color: QColor | None = None, rx_color: QColor | None = None):
        super().__init__(parent)

        self.tx_color = tx_color
        self.rx_color = rx_color

    def paint(self, painter, option, index):
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)

        col = index.column()

        if col == HexViewModel.Col_Index_Direction:
            self.paint_direction(painter, opt, index)
            return

        super().paint(painter, opt, index)

    def paint_direction(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex):
        model = cast(HexViewModel, index.model())
        row_data = model.get_row_data(index.row())

        # 创建 option 的副本，避免直接修改传入的原始 option 对象
        opt = QStyleOptionViewItem(option)

        if row_data.direction == HexViewDirection.TX:
            color = self.tx_color
        elif row_data.direction == HexViewDirection.RX:
            color = self.rx_color
        else:
            raise ValueError

        if color:
            for group in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive):
                opt.palette.setColor(group, QPalette.ColorRole.Text, color)
                opt.palette.setColor(group, QPalette.ColorRole.HighlightedText, color)

        super().paint(painter, opt, index)
