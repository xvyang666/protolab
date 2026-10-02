# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'serial_page.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_SerialPage(object):
    def setupUi(self, SerialPage):
        if not SerialPage.objectName():
            SerialPage.setObjectName(u"SerialPage")
        SerialPage.resize(639, 457)
        self.verticalLayout_2 = QVBoxLayout(SerialPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(SerialPage)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.refresh_btn = QPushButton(self.widget)
        self.refresh_btn.setObjectName(u"refresh_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_btn.sizePolicy().hasHeightForWidth())
        self.refresh_btn.setSizePolicy(sizePolicy)
        self.refresh_btn.setMinimumSize(QSize(36, 36))
        self.refresh_btn.setMaximumSize(QSize(24, 36))

        self.horizontalLayout.addWidget(self.refresh_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.com_list = QListWidget(self.widget)
        self.com_list.setObjectName(u"com_list")

        self.verticalLayout.addWidget(self.com_list)

        self.splitter.addWidget(self.widget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.splitter.addWidget(self.tabWidget)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(SerialPage)

        QMetaObject.connectSlotsByName(SerialPage)
    # setupUi

    def retranslateUi(self, SerialPage):
        SerialPage.setWindowTitle(QCoreApplication.translate("SerialPage", u"Form", None))
        self.refresh_btn.setText("")
    # retranslateUi

