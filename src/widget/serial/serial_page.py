import asyncio
import re

from PySide6.QtCore import Qt
from PySide6.QtSerialPort import QSerialPortInfo
from PySide6.QtWidgets import QWidget, QListWidgetItem

from bus.obj import theme, logger
from theme.icon import Icon
from ui.serial.serial_page import Ui_SerialPage
from widget.serial.serial_item import SerialItem


class SerialPage(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.ui = Ui_SerialPage()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.refresh_btn.setIcon(theme.get_icon(Icon.refresh))

        self.ui.refresh_btn.clicked.connect(lambda: asyncio.create_task(self.refresh_com_list()))

        asyncio.create_task(self.refresh_com_list())

    async def refresh_com_list(self):
        self.ui.refresh_btn.setEnabled(False)

        try:
            port_info_list = await asyncio.to_thread(QSerialPortInfo.availablePorts)

            names: list[str] = []
            for info in port_info_list:
                names.append(info.portName())

            names.sort(key=lambda x: int(match.group()) if (match := re.search(r'\d+', x)) else 0)

            self.ui.com_list.clear()
            for name in names:
                custom_widget = SerialItem(self, name)
                item = QListWidgetItem(self.ui.com_list)
                item.setSizeHint(custom_widget.sizeHint())
                item.setData(Qt.ItemDataRole.UserRole, name)
                self.ui.com_list.setItemWidget(item, custom_widget)

        except Exception as e:
            logger.default.error(e)

        self.ui.refresh_btn.setEnabled(True)

    def conn_success(self, port_name: str):
        print(port_name)
