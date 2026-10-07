from PySide6.QtCore import QAbstractTableModel, QObject, QModelIndex, Qt

from comp.hex_data_view.types import HexViewRowData


class HexViewModel(QAbstractTableModel):
    Col_Len = 5

    Col_Index_Num = 0
    Col_Index_Direction = 1
    Col_Index_Time = 2
    Col_Index_Data = 3
    Col_Index_Size = 4

    Default_Width = [50, 60, 180, 300, 100]
    Header_Text = ['序号', '方向', '时间戳', 'Hex', '大小']
    Header_Tooltip = ['行索引', '发送还是接收', '接收到数据的时间', '十六进制原始数据', '原始数据字节数']

    assert Col_Len == len(Default_Width) == len(Header_Text) == len(Header_Tooltip)

    Data_Max_Len = 256

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.__data: list[HexViewRowData] = []

    def rowCount(self, /, parent=...):
        return len(self.__data)

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
            row_data = self.__data[index.row()]
            row, col = index.row(), index.column()

            if col == self.Col_Index_Num:
                return str(row + 1)

            elif col == self.Col_Index_Direction:
                return row_data.direction.name

            elif col == self.Col_Index_Time:
                return row_data.date_time.astimezone().strftime('%Y-%m-%d %H:%M:%S.%f')

            elif col == self.Col_Index_Data:
                return f'{row_data.bytes_data[:self.Data_Max_Len].hex(' ')}{"..." if len(row_data.bytes_data) > self.Data_Max_Len else ""}'

            elif col == self.Col_Index_Size:
                return f'{len(row_data.bytes_data):,}'

            else:
                raise ValueError

        return None

    def get_row_data(self, row: int) -> HexViewRowData:
        return self.__data[row]

    def append_row(self, *row: HexViewRowData):
        start = len(self.__data)
        end = start + len(row) - 1

        self.beginInsertRows(QModelIndex(), start, end)
        self.__data.extend(row)
        self.endInsertRows()

    def clear_all(self):
        start = 0
        end = len(self.__data) - 1

        self.beginRemoveRows(QModelIndex(), start, end)
        self.__data.clear()
        self.endRemoveRows()

    def get_data(self) -> list[HexViewRowData]:
        return self.__data
