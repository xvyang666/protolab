import asyncio

import serial
import serial_asyncio


class AsyncSerial:
    def __init__(self, port: str, baudrate: int = 9600, databytes: int = serial.EIGHTBITS, stopbits: int = serial.STOPBITS_ONE, parity: str = serial.PARITY_NONE):
        self.port = port
        self.baudrate = baudrate
        self.databytes = databytes
        self.stopbits = stopbits
        self.parity = parity

        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    async def open(self):
        """打开串口"""
        self._reader, self._writer = await serial_asyncio.open_serial_connection(
            url=self.port,
            baudrate=self.baudrate,
            databytes=self.databytes,
            stopbits=self.stopbits,
            parity=self.parity,
        )

    async def write(self, data: bytes):
        """发送字节数据 (自动 drain)"""
        if not self._writer or self._writer.is_closing():
            raise RuntimeError("Serial connection is not open.")

        self._writer.write(data)
        await self._writer.drain()

    async def read(self, n: int = -1) -> bytes:
        """读取指定字节数"""
        if not self._reader:
            raise RuntimeError("Serial connection is not open.")

        return await self._reader.read(n)

    async def readline(self) -> bytes:
        """读取一行数据"""
        if not self._reader:
            raise RuntimeError("Serial connection is not open.")

        return await self._reader.readline()

    async def close(self):
        """关闭串口连接"""
        if self._writer and not self._writer.is_closing():
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass

    def is_open(self) -> bool:
        """检查连接状态"""
        return self._writer is not None and not self._writer.is_closing()

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
