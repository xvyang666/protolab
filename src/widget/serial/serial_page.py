import asyncio
import re

from PySide6.QtCore import Qt
from PySide6.QtSerialPort import QSerialPortInfo
from PySide6.QtWidgets import QWidget, QListWidgetItem

from bus.obj import theme, logger
from bus.serial_conn_manage import serial_conn_manage
from theme.icon import Icon
from ui.serial.serial_page import Ui_SerialPage
from widget.serial.serial_item import SerialItem
from widget.serial.serial_panel import SerialPanel


class SerialPage(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.ui = Ui_SerialPage()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.refresh_btn.setIcon(theme.get_icon(Icon.refresh))

        self.ui.com_list.currentItemChanged.connect(self.串口列表的选中项变化)
        self.ui.tabWidget.currentChanged.connect(self.串口面板tab选中项变化)
        self.ui.tabWidget.tabCloseRequested.connect(self.串口面板tab页关闭)
        self.ui.refresh_btn.clicked.connect(lambda: asyncio.create_task(self.刷新串口列表()))

        self.panel_map: dict[str, SerialPanel] = {}

        asyncio.create_task(self.刷新串口列表())

        serial_conn_manage.conn_changed_signal.connect(self.串口管理器变化)

    async def 刷新串口列表(self):
        self.ui.refresh_btn.setEnabled(False)

        try:
            port_info_list = await asyncio.to_thread(QSerialPortInfo.availablePorts)

            names: list[str] = []
            for info in port_info_list:
                names.append(info.portName())

            names.sort(key=lambda x: int(match.group()) if (match := re.search(r'\d+', x)) else 0)

            # 重建前记住当前选中的名字
            last_select_name: str | None = None
            last_item: QListWidgetItem | None = self.ui.com_list.currentItem()
            if last_item:
                last_select_name = last_item.data(Qt.ItemDataRole.UserRole)

            # 重建开始, 阻止发射不必要的信号
            self.ui.com_list.blockSignals(True)

            # 用于在循环中记住对应的 item
            target_item: QListWidgetItem | None = None

            self.ui.com_list.clear()
            for name in names:
                custom_widget = SerialItem(self, name)
                item = QListWidgetItem(self.ui.com_list)
                item.setSizeHint(custom_widget.sizeHint())
                item.setData(Qt.ItemDataRole.UserRole, name)
                self.ui.com_list.setItemWidget(item, custom_widget)

                if name == last_select_name:
                    target_item = item

            # 重建结束, 恢复信号
            self.ui.com_list.blockSignals(False)

            # 恢复之前的点击状态, 如果找不到就选中第一个
            if target_item:
                self.ui.com_list.setCurrentItem(target_item)
            else:
                if self.ui.com_list.count() > 0:
                    self.ui.com_list.setCurrentRow(0)

        except Exception as e:
            logger.default.exception(e)

        self.ui.refresh_btn.setEnabled(True)

    def 串口列表的选中项变化(self, item: QListWidgetItem):
        if item is None:
            return

        name: str = item.data(Qt.ItemDataRole.UserRole)
        self.创建串口面板并选中(name)

    def 串口管理器变化(self, name: str, _conned: bool):
        if _conned:
            self.创建串口面板并选中(name)

    def 创建串口面板并选中(self, name: str):
        panel = self.panel_map.get(name)
        if not panel:
            panel = SerialPanel(self, name)
            self.panel_map[name] = panel
            self.ui.tabWidget.addTab(panel, name)

        self.ui.tabWidget.setCurrentWidget(panel)

    def 串口面板tab选中项变化(self, index: int):
        if index < 0:
            return

        current_widget: SerialPanel = self.ui.tabWidget.widget(index)

        # 遍历 com_list 匹配对应的 item, 反向选中 列表, 保持两边的同步
        for i in range(self.ui.com_list.count()):
            item = self.ui.com_list.item(i)

            if item.data(Qt.ItemDataRole.UserRole, Qt.ItemDataRole.DisplayRole) == current_widget.name:
                self.ui.com_list.blockSignals(True)
                self.ui.com_list.setCurrentItem(item)
                self.ui.com_list.blockSignals(False)
                break

    def 串口面板tab页关闭(self, index: int):
        if index < 0:
            return

        current_widget: SerialPanel = self.ui.tabWidget.widget(index)
        self.panel_map.pop(current_widget.name)
        current_widget.deleteLater()

        list_item = self.ui.com_list.currentItem()
        if list_item.data(Qt.ItemDataRole.UserRole, Qt.ItemDataRole.DisplayRole) == current_widget.name:
            self.ui.com_list.blockSignals(True)
            self.ui.com_list.setCurrentItem(None)
            self.ui.com_list.blockSignals(False)
