from PySide6.QtSerialPort import QSerialPort
from PySide6.QtWidgets import QWidget, QDialog

from config.setting import setting
from model.SerialConnConfig import SerialConnConfig
from ui.serial.serial_item_setting import Ui_SerialItemSetting
from util.combobox_set_default import combobox_set_default


class SerialItemSetting(QDialog):
    def __init__(self, parent: QWidget, cfg: SerialConnConfig):
        super().__init__(parent)
        self.ui = Ui_SerialItemSetting()
        self.ui.setupUi(self)
        self.ui.port_name_label.setText(cfg.name)
        self.setWindowTitle(self.tr('串口设置'))

        self.name = cfg.name

        for i in setting.serial_baud_rate_list:
            self.ui.baud_rate_select.addItem(str(i), i)

        for i in QSerialPort.DataBits:
            self.ui.data_bit_select.addItem(_DATA_BITS_text[i], i)

        for i in QSerialPort.StopBits:
            self.ui.stop_bit_select.addItem(_STOP_BITS_text[i], i)

        for i in QSerialPort.Parity:
            self.ui.parity_select.addItem(_PARITY_text[i], i)

        # 设置默认值
        for c, v in [
            (self.ui.baud_rate_select, cfg.baud_rate),
            (self.ui.data_bit_select, cfg.data_bit),
            (self.ui.stop_bit_select, cfg.stop_bit),
            (self.ui.parity_select, cfg.parity),
        ]:
            combobox_set_default(c, v)

    def get_cfg(self):
        name = self.name
        baud_rate: QSerialPort.BaudRate = self.ui.baud_rate_select.currentData()
        data_bit: QSerialPort.DataBits = self.ui.data_bit_select.currentData()
        stop_bit: QSerialPort.StopBits = self.ui.stop_bit_select.currentData()
        parity: QSerialPort.Parity = self.ui.parity_select.currentData()

        return SerialConnConfig(
            name=name,
            baud_rate=baud_rate,
            data_bit=data_bit,
            stop_bit=stop_bit,
            parity=parity,
        )

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
    QSerialPort.Parity.NoParity: "None (无校验)",
    QSerialPort.Parity.EvenParity: "Even (偶校验)",
    QSerialPort.Parity.OddParity: "Odd (奇校验)",
    QSerialPort.Parity.SpaceParity: "Space (空格)",
    QSerialPort.Parity.MarkParity: "Mark (标记)",
}
