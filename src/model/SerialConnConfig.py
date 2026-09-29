from PySide6.QtSerialPort import QSerialPort
from pydantic import BaseModel


class SerialConnConfig(BaseModel):
    name: str
    baud_rate: int
    data_bit: QSerialPort.DataBits
    stop_bit: QSerialPort.StopBits
    parity: QSerialPort.Parity
