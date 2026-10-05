from datetime import datetime, timezone

from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor
from PySide6.QtSerialPort import QSerialPort
from PySide6.QtWidgets import QWidget, QAbstractButton, QRadioButton

from bus.global_ref import GlobalRef
from bus.obj import theme
from bus.serial_conn_manage import serial_conn_manage
from comp.EnterSubmitPlainTextEdit import EnterTextEdit
from comp.hex_data_view.types import HexViewRowData, HexViewDirection
from comp.hex_data_view.widget import HexViewWidget
from config.setting import setting
from model.SerialSendConfig import SerialSendConfig
from theme.icon import Icon
from ui.serial.serial_panel import Ui_SerialPanel


class SerialPanel(QWidget):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.ui = Ui_SerialPanel()
        self.ui.setupUi(self)
        self.ui.port_label.setText(name)
        self.ui.send_btn.setIcon(theme.get_icon(Icon.send))
        self.ui.splitter.setSizes([9999, 0])
        self.hex_view = HexViewWidget(
            f'{name}.txt',
            QColor(theme.color.primary.main),
            QColor(theme.color.secondary.main),
            self
        )
        self.ui.log_layout.addWidget(self.hex_view)

        self.input = EnterTextEdit(self)
        self.ui.input_layout.addWidget(self.input)

        self.name = name
        self.conn: QSerialPort | None = None
        self.max_timeout: int = 30  # 最长等多久算一个包, 避免一直有包进入导致一直无法输出
        self.max_buf_size: int = 1024 * 10  # 最多收集多少数据就输出一次, 避免无限膨胀
        self.buffer: bytearray = bytearray()  # 缓冲区
        self.timer = QTimer(self)

        self.send_cfg: SerialSendConfig = setting.serial_send_config.get(name)
        if not self.send_cfg:
            self.send_cfg = SerialSendConfig(
                append_mode=SerialSendConfig.AppendMode.none,
                send_mode=SerialSendConfig.SendMode.str,
            )

        self.send_mode_ui_to_value: dict[QRadioButton, SerialSendConfig.SendMode] = {
            self.ui.radio_btn_send_mode_str: SerialSendConfig.SendMode.str,
            self.ui.radio_btn_send_mode_hex: SerialSendConfig.SendMode.hex,
        }

        self.append_mode_ui_to_value: dict[QRadioButton, SerialSendConfig.AppendMode] = {
            self.ui.radio_btn_append_mode_none: SerialSendConfig.AppendMode.none,
            self.ui.radio_btn_append_mode_rn: SerialSendConfig.AppendMode.rn,
            self.ui.radio_btn_append_mode_r: SerialSendConfig.AppendMode.r,
            self.ui.radio_btn_append_mode_n: SerialSendConfig.AppendMode.n,
        }

        send_mode_value_to_ui = {v: k for k, v in self.send_mode_ui_to_value.items()}
        send_mode_value_to_ui[self.send_cfg.send_mode].setChecked(True)

        append_mode_value_to_ui = {v: k for k, v in self.append_mode_ui_to_value.items()}
        append_mode_value_to_ui[self.send_cfg.append_mode].setChecked(True)

        serial_conn_manage.conn_changed_signal.connect(self.串口管理器状态变化)
        self.ui.radio_btn_group_append_mode.buttonClicked.connect(self.追加模式变化)
        self.ui.radio_btn_group_send_mode.buttonClicked.connect(self.发送模式变化)
        self.ui.send_btn.clicked.connect(self.发送按钮被点击)
        self.input.submitted.connect(self.send_data)

        self.初始化连接()

    def 串口管理器状态变化(self, name: str, _conned: bool):
        if name != self.name:
            return

        self.初始化连接()

    def 初始化连接(self):
        self.conn = serial_conn_manage.get_conn(self.name)
        if not self.conn:
            return

        self.conn.readyRead.connect(self.read_data)

    def read_data(self):
        if not self.conn:
            return

        data = self.conn.readAll().data()
        self.buffer += data

        if len(self.buffer) > self.max_buf_size:
            self.输出到界面()
            return

        self.timer.singleShot(self.max_timeout, self.输出到界面)

    def 输出到界面(self):
        data = bytes(self.buffer)
        self.buffer.clear()

        self.hex_view.append_row(
            HexViewRowData(
                date_time=datetime.now(timezone.utc),
                bytes_data=data,
                direction=HexViewDirection.RX,
            )
        )

    def 追加模式变化(self, btn: QAbstractButton):
        assert isinstance(btn, QRadioButton)
        self.send_cfg.append_mode = self.append_mode_ui_to_value[btn]
        setting.serial_send_config[self.name] = self.send_cfg

    def 发送模式变化(self, btn: QAbstractButton):
        assert isinstance(btn, QRadioButton)
        self.send_cfg.send_mode = self.send_mode_ui_to_value[btn]
        setting.serial_send_config[self.name] = self.send_cfg

    def 发送按钮被点击(self):
        src_text = self.input.toPlainText()
        self.send_data(src_text)

    def send_data(self, s: str):
        if not s:
            return

        if self.send_cfg.send_mode == SerialSendConfig.SendMode.str:
            data = s.encode()
        elif self.send_cfg.send_mode == SerialSendConfig.SendMode.hex:
            try:
                data = bytes.fromhex(s)
            except:
                GlobalRef.main_window_notifier.warning(self.tr('请输入有效的 hex 数据'))
                return
        else:
            raise ValueError

        if self.send_cfg.append_mode == SerialSendConfig.AppendMode.none:
            ...
        elif self.send_cfg.append_mode == SerialSendConfig.AppendMode.rn:
            data = data + b'\r\n'
        elif self.send_cfg.append_mode == SerialSendConfig.AppendMode.r:
            data = data + b'\r'
        elif self.send_cfg.append_mode == SerialSendConfig.AppendMode.n:
            data = data + b'\n'
        else:
            raise ValueError

        if self.conn:
            self.conn.write(data)
            self.hex_view.append_row(
                HexViewRowData(
                    date_time=datetime.now(timezone.utc),
                    bytes_data=data,
                    direction=HexViewDirection.TX,
                )
            )
        else:
            GlobalRef.main_window_notifier.warning(self.tr('串口 {} 未连接').format(self.name))
            return

        self.input.setPlainText('')
