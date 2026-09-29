from PySide6.QtCore import Signal, QObject
from PySide6.QtSerialPort import QSerialPort


class _SerialConnManage(QObject):
    conn_changed_signal = Signal(str, bool)

    _all_conn: dict[str, QSerialPort] = {}
    """ 存放的是存活的连接 """

    def get_conn(self, name: str) -> QSerialPort | None:
        return self._all_conn.get(name)

    def is_open(self, name: str) -> bool:
        return name in self._all_conn

    def close_conn(self, name: str):
        conn = self._all_conn.pop(name)
        conn.close()
        self.conn_changed_signal.emit(name, False)

    def add_conn(self, name: str, conn: QSerialPort):
        conn.errorOccurred.connect(lambda err: self.on_serial_error(name, err))

        self._all_conn[name] = conn
        self.conn_changed_signal.emit(name, True)

    def on_serial_error(self, name: str, error: QSerialPort.SerialPortError):
        if error in (
                QSerialPort.SerialPortError.ResourceError,
                QSerialPort.SerialPortError.DeviceNotFoundError,
                QSerialPort.SerialPortError.PermissionError
        ):
            self.close_conn(name)


serial_conn_manage: _SerialConnManage = _SerialConnManage()
