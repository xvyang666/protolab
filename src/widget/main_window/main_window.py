from enum import Enum
from typing import Callable

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, Qt, QActionGroup
from PySide6.QtWidgets import QWidget, QMainWindow, QStackedWidget

from bus.obj import theme
from config.setting import setting
from theme.icon import Icon, IconEnum
from widget.serial.serial_page import SerialPage
from widget.setting.setting_page import SettingPage


class PageData:
    def __init__(self, icon: IconEnum, title: str, page_factory: Callable[[QWidget], QWidget]):
        self.icon = icon
        self.title = title
        self.page_factory = page_factory
        self.page_object: QWidget | None = None


class Page(Enum):
    串口 = '串口'
    modbus = 'modbus'
    mqtt = 'mqtt'
    tcp = 'tcp'
    udp = 'udp'
    设置 = '设置'


All_Page_Data: dict[Page, PageData] = {
    Page.串口: PageData(icon=Icon.serial, title='串口', page_factory=SerialPage),
    Page.modbus: PageData(icon=Icon.modbus, title='Modbus', page_factory=QWidget),
    Page.mqtt: PageData(icon=Icon.mqtt, title='Mqtt', page_factory=QWidget),
    Page.tcp: PageData(icon=Icon.tcp, title='Tcp', page_factory=QWidget),
    Page.udp: PageData(icon=Icon.udp, title='Udp', page_factory=QWidget),
    Page.设置: PageData(icon=Icon.settings, title='设置', page_factory=SettingPage),
}
assert len(Page) == len(All_Page_Data), '缺少配置'

Main_Page = [
    Page.串口,
    # Page.modbus,
    # Page.mqtt,
    # Page.tcp,
    # Page.udp,
]


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr('protolab'))
        self.setWindowIcon(theme.get_icon(Icon.app_icon))
        self.stacked_widget: QStackedWidget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # 初始化位置
        self.resize(setting.main_window_loc.w, setting.main_window_loc.h)
        self.move(setting.main_window_loc.x, setting.main_window_loc.y)

        self.init_meau_and_tool_bar()

    def init_meau_and_tool_bar(self):
        # 主功能
        name = self.tr('主功能')

        主功能_menu = self.menuBar().addMenu(name)

        主功能_tool_bar = self.addToolBar(name)
        主功能_tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        主功能_tool_bar.setIconSize(QSize(32, 32))

        # 单选组
        action_group = QActionGroup(self)
        action_group.setExclusive(True)

        for k in Main_Page:
            v = All_Page_Data[k]
            action = QAction(theme.get_icon(v.icon), self.tr(v.title), self)
            action.setCheckable(True)
            action.triggered.connect(lambda _, _k=k: self.点击功能(_k))

            action_group.addAction(action)

            主功能_menu.addAction(action)
            主功能_tool_bar.addAction(action)

            if k == Page.串口:
                action.setChecked(True)
                self.点击功能(k)

        # 选项
        选项_menu = self.menuBar().addMenu(self.tr('选项'))

        k = Page.设置
        v = All_Page_Data[k]
        se_action = QAction(theme.get_icon(v.icon), self.tr(v.title), self)
        se_action.triggered.connect(lambda _, _k=k: self.点击功能(_k))
        选项_menu.addAction(se_action)

    def 点击功能(self, k: Page):
        data = All_Page_Data[k]
        if data.page_object is None:
            data.page_object = data.page_factory(self)

        assert data.page_object

        if k in Main_Page:
            self.stacked_widget.addWidget(data.page_object)
            self.stacked_widget.setCurrentWidget(data.page_object)

        elif k == Page.设置:
            data.page_object.show()

        else:
            raise ValueError

    def closeEvent(self, event, /):
        setting.main_window_loc.x = self.x()
        setting.main_window_loc.y = self.y()
        setting.main_window_loc.w = self.width()
        setting.main_window_loc.h = self.height()
        setting.save()

        super().closeEvent(event)
