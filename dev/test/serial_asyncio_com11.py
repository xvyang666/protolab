import asyncio
import serial_asyncio

async def send_task(writer: asyncio.StreamWriter):
    """异步发送任务"""
    count = 0
    try:
        while True:
            message = f"Ping {count}\n"
            print(f"[Send] {message.strip()}")
            writer.write(message.encode("utf-8"))
            await writer.drain()  # 确保数据已刷入串口硬件发送缓冲区
            count += 1
            await asyncio.sleep(2)  # 每隔 2 秒发送一次
    except asyncio.CancelledError:
        print("Send task cancelled.")

async def recv_task(reader: asyncio.StreamReader):
    """异步接收任务"""
    try:
        while True:
            # readline() 会一直等待直到读取到 '\n'
            # 如果是固定字节流, 可以使用 await reader.read(1024)
            data = await reader.readline()
            if data:
                text = data.decode("utf-8", errors="ignore").strip()
                print(f"[Recv] {text}")
    except asyncio.CancelledError:
        print("Recv task cancelled.")

async def main():
    # 根据实际情况修改串口号和波特率
    # Windows 示例: 'COM3'
    # Linux / Mac 示例: '/dev/ttyUSB0' 或 '/dev/tty.usbserial-1410'
    port = "COM11"
    baudrate = 9600

    print(f"Opening serial port {port} at {baudrate} baud...")

    # 打开串口连接, 获取 reader 和 writer
    reader, writer = await serial_asyncio.open_serial_connection(
        url=port,
        baudrate=baudrate,
        bytesize=8,
        stopbits=1,
        parity='N'
    )
    print("Serial port opened successfully!")

    # 创建并发收发任务
    # task_send = asyncio.create_task(send_task(writer))
    task_recv = asyncio.create_task(recv_task(reader))

    # 并行运行任务
    await asyncio.gather( task_recv)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting program...")