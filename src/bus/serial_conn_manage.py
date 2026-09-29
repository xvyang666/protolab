from PySide6.QtSerialPort import QSerialPort


class SerialConnManage:
    _all_conn: dict[str, QSerialPort] = {}
    """ 存放的是存活的连接 """

    @classmethod
    def get_conn(cls, port_name: str) -> QSerialPort | None:
        return cls._all_conn.get(port_name)

    @classmethod
    def close_conn(cls, port_name: str):
        conn = cls._all_conn.pop(port_name)
        conn.close()

    @classmethod
    def add_conn(cls, port_name: str, conn: QSerialPort):
        cls._all_conn[port_name] = conn


