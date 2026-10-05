import asyncio

from PySide6.QtCore import Signal, QObject
from PySide6.QtSerialPort import QSerialPort

from bus.global_ref import GlobalRef


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

    async def add_conn(
            self,
            name: str,
            baudRate: int,
            dataBits: QSerialPort.DataBits,
            stopBits: QSerialPort.StopBits,
            parity: QSerialPort.Parity,
    ) -> QSerialPort | None:

        def _create_and_open():
            # 由于 open 是阻塞操作, 这里在子线程中创建 QSerialPort
            # 但后续的 read/write 逻辑直接在主线程调用的, 这个跨线程使用会有bug, 这里创建并连接后再移交到主线程
            _conn = QSerialPort(
                name,
                baudRate=baudRate,
                dataBits=dataBits,
                stopBits=stopBits,
                parity=parity,
            )

            ok = _conn.open(QSerialPort.OpenModeFlag.ReadWrite)
            if not ok:
                return None

            main_thread = GlobalRef.app.thread()
            _conn.moveToThread(main_thread)
            return _conn

        conn = await asyncio.to_thread(_create_and_open)
        if not conn:
            return None

        conn.errorOccurred.connect(lambda err: self.on_serial_error(name, err))
        self._all_conn[name] = conn
        self.conn_changed_signal.emit(name, True)
        return conn

    def on_serial_error(self, name: str, error: QSerialPort.SerialPortError):
        if error in (
                QSerialPort.SerialPortError.ResourceError,
                QSerialPort.SerialPortError.DeviceNotFoundError,
                QSerialPort.SerialPortError.PermissionError
        ):
            self.close_conn(name)


serial_conn_manage: _SerialConnManage = _SerialConnManage()
