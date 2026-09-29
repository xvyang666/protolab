import sys

from PySide6.QtCore import QTimer, QDateTime, QObject, Signal
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout,
                               QPlainTextEdit, QPushButton)


class SerialFrameBuffer(QObject):
    """串口数据帧拼包器 (基于空闲超时机制)"""
    frame_ready = Signal(str, bytes)  # 发射信号: (时间戳字符串, 完整数据帧)

    def __init__(self, timeout_ms=30, max_buffer_size=1024, parent=None):
        super().__init__(parent)
        self.timeout_ms = timeout_ms
        self.max_buffer_size = max_buffer_size
        self.buffer = bytearray()

        # 空闲检测定时器
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(self.timeout_ms)
        self.timer.timeout.connect(self._flush)

    def append_data(self, chunk: bytes):
        """串口 readyRead 收到数据时调用此函数"""
        if not chunk:
            return

        self.buffer.extend(chunk)

        # 防爆仓机制: 超过最大尺寸直接强制输出, 避免高频大数据占用过大内存
        if len(self.buffer) >= self.max_buffer_size:
            self._flush()
        else:
            # 重新打断并重置定时器 (只要在 timeout_ms 内有持续数据, 就不断帧)
            self.timer.start()

    def _flush(self):
        self.timer.stop()
        if not self.buffer:
            return

        # 获取毫秒级时间戳: 14:20:05.123
        timestamp = QDateTime.currentDateTime().toString("HH:mm:ss.zzz")
        data = bytes(self.buffer)
        self.buffer.clear()

        self.frame_ready.emit(timestamp, data)


class TripleHexAsciiViewer(QWidget):
    """带时间戳的 Hex / ASCII 三列联动查看器"""
    BYTES_PER_LINE = 16

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_syncing = False
        self.frames = []  # 存储数据帧记录 [(timestamp, bytes_data)]

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # 1. 时间戳列
        self.time_edit = QPlainTextEdit()
        self.time_edit.setReadOnly(True)
        self.time_edit.setFixedWidth(140)
        self.time_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        # 2. Hex 列
        self.hex_edit = QPlainTextEdit()
        self.hex_edit.setReadOnly(True)
        self.hex_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        # 3. ASCII 列
        self.ascii_edit = QPlainTextEdit()
        self.ascii_edit.setReadOnly(True)
        self.ascii_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        # 统一使用等宽字体
        font = QFont("Consolas", 10)
        for edit in (self.time_edit, self.hex_edit, self.ascii_edit):
            edit.setFont(font)

        layout.addWidget(self.time_edit, stretch=0)
        layout.addWidget(self.hex_edit, stretch=2)
        layout.addWidget(self.ascii_edit, stretch=1)

    def _connect_signals(self):
        # 滚动条三向绑定
        sb_time = self.time_edit.verticalScrollBar()
        sb_hex = self.hex_edit.verticalScrollBar()
        sb_ascii = self.ascii_edit.verticalScrollBar()

        sb_hex.valueChanged.connect(sb_time.setValue)
        sb_hex.valueChanged.connect(sb_ascii.setValue)
        sb_time.valueChanged.connect(sb_hex.setValue)
        sb_ascii.valueChanged.connect(sb_hex.setValue)

        # 光标选中同步
        self.hex_edit.selectionChanged.connect(self._on_hex_selection_changed)
        self.ascii_edit.selectionChanged.connect(self._on_ascii_selection_changed)

    def add_frame(self, timestamp: str, data: bytes):
        """追加一帧带有时间戳的数据"""
        self.frames.append((timestamp, data))

        # 计算这一帧需要拆成几行 (每 16 字节一行)
        total_bytes = len(data)
        lines_count = (total_bytes + self.BYTES_PER_LINE - 1) // self.BYTES_PER_LINE
        if lines_count == 0:
            lines_count = 1

        # 1. 生成时间戳文本 (只有第一行显示时间戳, 后续多行显示空位, 保持对齐)
        time_text_list = [f"[{timestamp}]"] + [" "] * (lines_count - 1)
        time_str = "\n".join(time_text_list)

        # 2. 生成 Hex 文本
        hex_lines = []
        ascii_lines = []

        for i in range(0, total_bytes, self.BYTES_PER_LINE):
            chunk = data[i:i + self.BYTES_PER_LINE]

            hex_part = " ".join(f"{b:02X}" for b in chunk)
            if len(chunk) < self.BYTES_PER_LINE:
                hex_part += "   " * (self.BYTES_PER_LINE - len(chunk))
            hex_lines.append(hex_part)

            ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
            ascii_lines.append(ascii_part)

        # 3. 追加到编辑框
        self._append_to_edit(self.time_edit, time_str)
        self._append_to_edit(self.hex_edit, "\n".join(hex_lines))
        self._append_to_edit(self.ascii_edit, "\n".join(ascii_lines))

    def _append_to_edit(self, edit: QPlainTextEdit, text: str):
        if not edit.toPlainText():
            edit.setPlainText(text)
        else:
            edit.appendPlainText(text)

    # ---------------- 选区同步逻辑 ----------------
    def _on_hex_selection_changed(self):
        if self._is_syncing:
            return
        self._is_syncing = True
        try:
            self._sync_selection(source=self.hex_edit, target=self.ascii_edit, is_hex_source=True)
        finally:
            self._is_syncing = False

    def _on_ascii_selection_changed(self):
        if self._is_syncing:
            return
        self._is_syncing = True
        try:
            self._sync_selection(source=self.ascii_edit, target=self.hex_edit, is_hex_source=False)
        finally:
            self._is_syncing = False

    def _sync_selection(self, source: QPlainTextEdit, target: QPlainTextEdit, is_hex_source: bool):
        cursor = source.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # 根据字符坐标换算目标选区
        doc_src = source.document()
        doc_tgt = target.document()

        # 简单整行高亮同步
        blk_start = doc_src.findBlock(start).blockNumber()
        blk_end = doc_src.findBlock(end).blockNumber()

        tgt_cursor = target.textCursor()
        tgt_start_pos = doc_tgt.findBlockByNumber(blk_start).position()
        tgt_end_blk = doc_tgt.findBlockByNumber(blk_end)
        tgt_end_pos = tgt_end_blk.position() + tgt_end_blk.length() - 1

        tgt_cursor.setPosition(tgt_start_pos)
        tgt_cursor.setPosition(tgt_end_pos, QTextCursor.MoveMode.KeepAnchor)
        target.setTextCursor(tgt_cursor)


# ---------------- 测试主窗口 ----------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("串口调试 - 时间戳与防断包流式展示")
        self.resize(800, 450)

        layout = QVBoxLayout(self)

        self.viewer = TripleHexAsciiViewer()
        layout.addWidget(self.viewer)

        # 创建拼包器 (超时 30ms)
        self.frame_buffer = SerialFrameBuffer(timeout_ms=30)
        self.frame_buffer.frame_ready.connect(self.viewer.add_frame)

        # 模拟操作按钮
        btn_layout = QHBoxLayout()
        btn1 = QPushButton("模拟高频碎片数据 (验证 30ms 自动拼包)")
        btn1.clicked.connect(self.mock_fragmented_data)

        btn2 = QPushButton("模拟长数据不带 \\n (验证超时输出)")
        btn2.clicked.connect(self.mock_no_newline_data)

        btn_layout.addWidget(btn1)
        btn_layout.addWidget(btn2)
        layout.addLayout(btn_layout)

    def mock_fragmented_data(self):
        """模拟串口极高频率收到碎片数据 (如每隔 5ms 收到几个字节)"""
        data_chunks = [
            b"AT+CSQ\r",
            b"\n+CSQ: 3",
            b"1,99\r\n",
            b"OK\r\n"
        ]
        # 5ms 间隔发送 -> 拼包器会将它们合并为同一帧并打上单个时间戳!
        for i, chunk in enumerate(data_chunks):
            QTimer.singleShot(i * 5, lambda c=chunk: self.frame_buffer.append_data(c))

    def mock_no_newline_data(self):
        """模拟没有 \\n 的自定义二进制协议/长数据流"""
        raw_bytes = b"\xAA\x55\x01\x02\x03\x04Hello_ProtoLab_No_NewLine_Data_1234567890\xFF\xFE"
        self.frame_buffer.append_data(raw_bytes)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
