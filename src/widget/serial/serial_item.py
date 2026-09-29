from PySide6.QtCore import Signal
from PySide6.QtSerialPort import QSerialPort
from PySide6.QtWidgets import QWidget, QMessageBox

from bus.obj import theme
from bus.serial_conn_manage import serial_conn_manage
from config.setting import setting
from model.SerialConnConfig import SerialConnConfig
from theme.icon import Icon
from ui.serial.serial_item import Ui_SerialItem
from widget.serial.serial_item_setting import SerialItemSetting


class SerialItem(QWidget):
    conn_signal = Signal(str)

    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)

        self.ui = Ui_SerialItem()
        self.ui.setupUi(self)
        self.ui.setting_btn.setIcon(theme.get_icon(Icon.edit))

        self.name = name
        self.cfg: SerialConnConfig = setting.serial_connect_config.get(name)
        if not self.cfg:
            self.cfg = SerialConnConfig(
                name=name,
                baud_rate=QSerialPort.BaudRate.Baud9600,
                data_bit=QSerialPort.DataBits.Data8,
                stop_bit=QSerialPort.StopBits.OneStop,
                parity=QSerialPort.Parity.NoParity,
            )

        self.ui.name_label.setText(name)
        self.refresh_conn_state(name, serial_conn_manage.is_open(name))
        self.refresh_detail_label()

        self.ui.run_or_stop_btn.clicked.connect(self.连接_or_断连)
        self.ui.setting_btn.clicked.connect(self.setting_btn_clicked)

        serial_conn_manage.conn_changed_signal.connect(self.refresh_conn_state)

    def 连接_or_断连(self):
        if serial_conn_manage.is_open(self.name):
            serial_conn_manage.close_conn(self.name)

        else:
            conn = QSerialPort(
                self.cfg.name,
                baudRate=self.cfg.baud_rate,
                dataBits=self.cfg.data_bit,
                stopBits=self.cfg.stop_bit,
                parity=self.cfg.parity,
            )

            ok = conn.open(QSerialPort.OpenModeFlag.ReadWrite)
            if not ok:
                QMessageBox.warning(self, self.tr('连接失败'), self.tr('串口 {} 连接失败, 请刷新串口列表或检查是否被占用').format(self.cfg.name))
                return

            serial_conn_manage.add_conn(self.cfg.name, conn)

    def refresh_detail_label(self):
        self.ui.detal_label.setText(f'{self.cfg.baud_rate}/{_DATA_BITS_text[self.cfg.data_bit]}/{_STOP_BITS_text[self.cfg.stop_bit]}/{_PARITY_text[self.cfg.parity]}')

    def refresh_conn_state(self, name: str, conned: bool):
        if name != self.cfg.name:
            return

        if conned:
            state_icon = Icon.enable_dot
            btn_icon = Icon.stop
        else:
            state_icon = Icon.unable_dot
            btn_icon = Icon.run

        self.ui.icon_label.setPixmap(theme.get_icon(state_icon).pixmap(16, 16))
        self.ui.run_or_stop_btn.setIcon(theme.get_icon(btn_icon))

    def setting_btn_clicked(self):
        dialog = SerialItemSetting(self, self.cfg)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        new_cfg = dialog.get_cfg()

        self.cfg = new_cfg
        setting.serial_connect_config[self.name] = new_cfg
        self.refresh_detail_label()


_DATA_BITS_text = {
    QSerialPort.DataBits.Data5: "5",
    QSerialPort.DataBits.Data6: "6",
    QSerialPort.DataBits.Data7: "7",
    QSerialPort.DataBits.Data8: "8",
}

_STOP_BITS_text = {
    QSerialPort.StopBits.OneStop: "1",
    QSerialPort.StopBits.OneAndHalfStop: "1.5",
    QSerialPort.StopBits.TwoStop: "2",
}

_PARITY_text = {
    QSerialPort.Parity.NoParity: "N",
    QSerialPort.Parity.EvenParity: "E",
    QSerialPort.Parity.OddParity: "O",
    QSerialPort.Parity.SpaceParity: "S",
    QSerialPort.Parity.MarkParity: "M",
}
