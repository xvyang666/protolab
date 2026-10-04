import datetime
from enum import Enum
from typing import NamedTuple

from PySide6.QtCore import QAbstractTableModel, QObject, QModelIndex, Qt


class HexViewDirection(Enum):
    RX = 'RX'
    TX = 'TX'


class HexViewRowData(NamedTuple):
    date_time: datetime
    bytes_data: bytes
    direction: HexViewDirection


class HexViewModel(QAbstractTableModel):
    Col_Len = 5

    Col_Index_Num = 0
    Col_Index_Direction = 1
    Col_Index_Time = 2
    Col_Index_Data = 3
    Col_Index_Size = 4

    Default_Width = [50, 60, 160, 300, 100]
    Header_Text = ['序号', '方向', '时间戳', 'Hex', '大小']
    Header_Tooltip = ['行索引', '发送还是接收', '接收到数据的时间', '十六进制原始数据', '原始数据字节数']

    assert Col_Len == len(Default_Width) == len(Header_Text) == len(Header_Tooltip)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._data: list[HexViewRowData] = []

    def rowCount(self, /, parent=...):
        return len(self._data)

    def columnCount(self, /, parent=...):
        return self.Col_Len

    def headerData(self, section, orientation, /, role=...):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self.tr(self.Header_Text[section])

            elif role == Qt.ItemDataRole.ToolTipRole:
                return self.tr(self.Header_Tooltip[section])

            elif role == Qt.ItemDataRole.TextAlignmentRole:
                return Qt.AlignmentFlag.AlignLeft  # 表头对齐

        return None

    def data(self, index, /, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            row_data = self._data[index.row()]
            row, col = index.row(), index.column()

            if col == self.Col_Index_Num:
                return str(row + 1)

            elif col == self.Col_Index_Direction:
                return row_data.direction.name

            elif col == self.Col_Index_Time:
                ...  # Delegate 渲染

            elif col == self.Col_Index_Data:
                return row_data.bytes_data.hex(' ')

            elif col == self.Col_Index_Size:
                return f'{len(row_data.bytes_data):,}'

            else:
                raise ValueError

        return None

    def get_row_data(self, row: int) -> HexViewRowData:
        return self._data[row]

    def append_row(self, *row: HexViewRowData):
        start = len(self._data)
        end = start + len(row) - 1

        self.beginInsertRows(QModelIndex(), start, end)
        self._data.extend(row)
        self.endInsertRows()
