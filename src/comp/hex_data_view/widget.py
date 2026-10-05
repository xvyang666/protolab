import asyncio

import aiofiles
from PySide6.QtCore import Qt, QItemSelection, QSize
from PySide6.QtGui import QFontDatabase, QTextCursor, QColor, QPalette
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QToolBar, QTableView,
    QSplitter, QLabel, QPlainTextEdit, QFileDialog
)

from bus.obj import theme
from comp.hex_data_view.delegate import HexViewDelegate
from comp.hex_data_view.model import HexViewModel
from comp.read_only_text_edit import ReadOnlyTextEdit
from comp.hex_data_view.types import HexViewRowData, HexViewDirection
from theme.icon import Icon


class HexViewWidget(QWidget):

    def __init__(
            self,
            log_name: str = 'log',
            tx_color: QColor | None = None,
            rx_color: QColor | None = None,
            parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.log_name = log_name
        self.tx_color = tx_color
        self.rx_color = rx_color

        self.tx_count = 0
        self.rx_count = 0
        self.自动滚动到最后 = True

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        title_bar_layout = QHBoxLayout()
        main_layout.addLayout(title_bar_layout)

        self.tx_label = QLabel(self)
        if self.tx_color:
            palette = self.tx_label.palette()
            palette.setColor(QPalette.ColorRole.WindowText, self.tx_color)
            self.tx_label.setPalette(palette)

        self.rx_label = QLabel(self)
        if self.rx_color:
            palette = self.rx_label.palette()
            palette.setColor(QPalette.ColorRole.WindowText, self.rx_color)
            self.rx_label.setPalette(palette)

        title_bar_layout.addWidget(self.tx_label)
        title_bar_layout.addWidget(self.rx_label)

        title_bar_layout.addStretch()

        toolbar = QToolBar(self)
        title_bar_layout.addWidget(toolbar)

        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        scroll_down_action = toolbar.addAction(theme.get_icon(Icon.scroll_down), self.tr("自动滚动到最后"))
        scroll_down_action.setCheckable(True)
        scroll_down_action.setChecked(self.自动滚动到最后)
        scroll_down_action.toggled.connect(self._自动滚动到最后选项变化)

        toolbar.addAction(theme.get_icon(Icon.column), self.tr("重置默认列宽"), self._重置列宽)
        toolbar.addAction(theme.get_icon(Icon.download), self.tr("保存日志数据到文件"), lambda: asyncio.create_task(self._保存数据()))
        toolbar.addAction(theme.get_icon(Icon.delete), self.tr("清空数据"), self._清除全部数据)

        # 1. 上方部件: TableView
        self.table_view = QTableView(self)
        self.table_view_model = HexViewModel(self)
        self.table_view.setModel(self.table_view_model)
        self.table_view.setItemDelegate(HexViewDelegate(self.table_view, self.tx_color, self.rx_color))

        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.setHorizontalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
        self.table_view.setVerticalScrollMode(QTableView.ScrollMode.ScrollPerPixel)

        # 2. 下方部件: 水平 QSplitter 包裹 Hex View 和 ASCII View
        bottom_splitter = QSplitter(Qt.Orientation.Horizontal)
        bottom_splitter.setChildrenCollapsible(False)

        # Hex 区域
        hex_widget = QWidget(self)
        hex_container = QVBoxLayout(hex_widget)
        hex_container.setContentsMargins(0, 0, 0, 0)

        hex_header_layout = QHBoxLayout()
        hex_header_layout.addWidget(QLabel("Hex"))
        self.hex_count_label = QLabel(self)
        hex_header_layout.addWidget(self.hex_count_label)
        hex_header_layout.addStretch()
        hex_container.addLayout(hex_header_layout)

        self.hex_edit = ReadOnlyTextEdit(self)
        self.hex_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)  # 禁止自动换行
        hex_container.addWidget(self.hex_edit)

        # ASCII 区域
        ascii_widget = QWidget(self)
        ascii_container = QVBoxLayout(ascii_widget)
        ascii_container.setContentsMargins(0, 0, 0, 0)
        ascii_container.addWidget(QLabel("Ascii"))
        self.ascii_edit = ReadOnlyTextEdit(self)
        self.ascii_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)  # 禁止自动换行
        ascii_container.addWidget(self.ascii_edit)

        # 设置等宽字体
        monospace_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        monospace_font.setPointSize(10)
        self.hex_edit.setFont(monospace_font)
        self.ascii_edit.setFont(monospace_font)

        bottom_splitter.addWidget(hex_widget)
        bottom_splitter.addWidget(ascii_widget)
        bottom_splitter.setSizes([300, 120])

        # 3. 整体布局: 垂直 QSplitter (上方为 TableView，下方为 bottom_splitter)
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.setChildrenCollapsible(False)  # 不允许折叠

        main_splitter.addWidget(self.table_view)
        main_splitter.addWidget(bottom_splitter)

        # 比例拉伸设置: index 0 (table_view) 占比最大，index 1 (bottom_splitter) 占比小
        main_splitter.setStretchFactor(0, 2 ** 10)
        main_splitter.setStretchFactor(1, 1)

        main_layout.addWidget(main_splitter)

        self.table_view.selectionModel().selectionChanged.connect(self._当前选中的数据变化)

        # 光标位置改变或选择区域改变时统一更新同步与字节计数
        self.hex_edit.cursorPositionChanged.connect(self._更新偏移)
        self.hex_edit.cursorPositionChanged.connect(self._hex选中变化_同步ascii选中)
        self.ascii_edit.cursorPositionChanged.connect(self._ascii选中变化_同步hex选中)

        self._重置列宽()
        self._更新偏移()
        self._刷新tx_rx统计标签()

    def _自动滚动到最后选项变化(self, checked: bool):
        self.自动滚动到最后 = checked
        if checked:
            self.table_view.scrollToBottom()

    def _更新偏移(self):
        self.hex_count_label.setText(self.tr('索引: {}').format(self.hex_edit.textCursor().position() // 3))

    def _重置列宽(self):
        for index, w in enumerate(HexViewModel.Default_Width):
            self.table_view.setColumnWidth(index, w)

    def _当前选中的数据变化(self, selected: QItemSelection, _deselected: QItemSelection):
        indexes = selected.indexes()
        if not indexes:
            self.hex_edit.clear()
            self.ascii_edit.clear()
            return

        row = indexes[0].row()
        row_data = self.table_view_model.get_row_data(row)

        bytes_data = row_data.bytes_data
        per_line = 16

        hex_line_list = []
        ascii_line_list = []
        for i in range(0, len(bytes_data), per_line):
            batch = bytes_data[i:i + per_line]
            hex_line_list.append(batch.hex(' '))
            ascii_line_list.append("".join([chr(b) if 32 <= b <= 126 else "." for b in batch]))

        self.hex_edit.setPlainText('\n'.join(hex_line_list))
        self.ascii_edit.setPlainText('\n'.join(ascii_line_list))

    def _hex选中变化_同步ascii选中(self):
        """
        hex 格式是
        xx xx ... xx\n  3个为一小块 16*3=48
        xx xx

        ascii格式是:
        AAAAAAAAAAAAAAAA\n 16+1=17
        AA

        """
        cursor = self.hex_edit.textCursor()
        if not cursor.hasSelection():
            ascii_cursor = self.ascii_edit.textCursor()
            ascii_cursor.clearSelection()
            self.ascii_edit.setTextCursor(ascii_cursor)
            return

        sel_start = cursor.selectionStart()
        sel_end = cursor.selectionEnd()

        tmp_cursor = QTextCursor(self.hex_edit.document())

        tmp_cursor.setPosition(sel_start)
        start_row = tmp_cursor.blockNumber()
        start_col = tmp_cursor.positionInBlock()

        tmp_cursor.setPosition(sel_end)
        end_row = tmp_cursor.blockNumber()
        end_col = tmp_cursor.positionInBlock()

        # 如果开始时选中的第一个字符是空格, 向后一个位置才开始计算
        if (start_col + 1) % 3 == 0:
            start_col += 1

        # 如果结束时摸到下一个字节范围, 直接 +3 以全算
        if end_col % 3 != 0:
            end_col += 3

        ascii_start_pos_in_block = start_col // 3
        ascii_end_pos_in_block = end_col // 3

        ascii_doc = self.ascii_edit.document()
        ascii_start_pos = ascii_doc.findBlockByNumber(start_row).position() + ascii_start_pos_in_block
        ascii_end_pos = ascii_doc.findBlockByNumber(end_row).position() + ascii_end_pos_in_block

        self.ascii_edit.blockSignals(True)
        ascii_cursor = self.ascii_edit.textCursor()
        ascii_cursor.setPosition(ascii_start_pos)
        ascii_cursor.setPosition(ascii_end_pos, QTextCursor.MoveMode.KeepAnchor)
        self.ascii_edit.setTextCursor(ascii_cursor)
        self.ascii_edit.blockSignals(False)

    def _ascii选中变化_同步hex选中(self):
        cursor = self.ascii_edit.textCursor()
        if not cursor.hasSelection():
            hex_cursor = self.hex_edit.textCursor()
            hex_cursor.clearSelection()
            self.hex_edit.setTextCursor(hex_cursor)
            return

        sel_start = cursor.selectionStart()
        sel_end = cursor.selectionEnd()

        tmp_cursor = QTextCursor(self.ascii_edit.document())

        tmp_cursor.setPosition(sel_start)
        start_row = tmp_cursor.blockNumber()
        start_col = tmp_cursor.positionInBlock()

        tmp_cursor.setPosition(sel_end)
        end_row = tmp_cursor.blockNumber()
        end_col = tmp_cursor.positionInBlock()

        ascii_start_pos_in_block = start_col * 3
        ascii_end_pos_in_block = end_col * 3 - 1

        hex_doc = self.hex_edit.document()
        hex_start_pos = hex_doc.findBlockByNumber(start_row).position() + ascii_start_pos_in_block
        hex_end_pos = hex_doc.findBlockByNumber(end_row).position() + ascii_end_pos_in_block

        self.hex_edit.blockSignals(True)
        hex_cursor = self.hex_edit.textCursor()
        hex_cursor.setPosition(hex_start_pos)
        hex_cursor.setPosition(hex_end_pos, QTextCursor.MoveMode.KeepAnchor)
        self.hex_edit.setTextCursor(hex_cursor)
        self.hex_edit.blockSignals(False)

    def append_row(self, *row_data: HexViewRowData):
        for row in row_data:
            if row.direction == HexViewDirection.TX:
                self.tx_count += len(row.bytes_data)
            elif row.direction == HexViewDirection.RX:
                self.rx_count += len(row.bytes_data)
            else:
                raise ValueError

        self._刷新tx_rx统计标签()

        self.table_view_model.append_row(*row_data)

        if self.自动滚动到最后:
            self.table_view.scrollToBottom()

    def _清除全部数据(self):
        self.table_view_model.clear_all()
        self.tx_count = 0
        self.rx_count = 0

        self._刷新tx_rx统计标签()

    def _刷新tx_rx统计标签(self):
        self.tx_label.setText(f'TX: {self.tx_count}')
        self.rx_label.setText(f'RX: {self.rx_count}')

    async def _保存数据(self):
        file_path_str, _ = QFileDialog.getSaveFileName(
            self,
            "保存数据",
            self.log_name,
        )

        if not file_path_str:
            return

        async with aiofiles.open(file_path_str, "w", encoding="utf-8") as f:
            for row in self.table_view_model.get_data():
                timestamp = row.date_time.astimezone().isoformat()
                direction = row.direction.name
                hex_data = row.bytes_data.hex(" ")

                await f.write(f"[{timestamp}] [{direction}] {hex_data}\n")
