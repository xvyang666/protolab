# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'serial_item.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_SerialItem(object):
    def setupUi(self, SerialItem):
        if not SerialItem.objectName():
            SerialItem.setObjectName(u"SerialItem")
        SerialItem.resize(302, 60)
        self.gridLayout = QGridLayout(SerialItem)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(1)
        self.icon_label = QLabel(SerialItem)
        self.icon_label.setObjectName(u"icon_label")

        self.gridLayout.addWidget(self.icon_label, 0, 0, 2, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 2, 1)

        self.widget = QWidget(SerialItem)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.run_or_stop_btn = QPushButton(self.widget)
        self.run_or_stop_btn.setObjectName(u"run_or_stop_btn")
        self.run_or_stop_btn.setMinimumSize(QSize(32, 32))
        self.run_or_stop_btn.setMaximumSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.run_or_stop_btn)

        self.setting_btn = QPushButton(self.widget)
        self.setting_btn.setObjectName(u"setting_btn")
        self.setting_btn.setMinimumSize(QSize(32, 32))
        self.setting_btn.setMaximumSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.setting_btn)


        self.gridLayout.addWidget(self.widget, 0, 3, 2, 1)

        self.name_label = QLabel(SerialItem)
        self.name_label.setObjectName(u"name_label")
        font = QFont()
        font.setPointSize(12)
        self.name_label.setFont(font)

        self.gridLayout.addWidget(self.name_label, 0, 1, 1, 1)

        self.detal_label = QLabel(SerialItem)
        self.detal_label.setObjectName(u"detal_label")
        font1 = QFont()
        font1.setPointSize(8)
        self.detal_label.setFont(font1)

        self.gridLayout.addWidget(self.detal_label, 1, 1, 1, 1)


        self.retranslateUi(SerialItem)

        QMetaObject.connectSlotsByName(SerialItem)
    # setupUi

    def retranslateUi(self, SerialItem):
        SerialItem.setWindowTitle(QCoreApplication.translate("SerialItem", u"Form", None))
        self.icon_label.setText(QCoreApplication.translate("SerialItem", u"icon", None))
        self.run_or_stop_btn.setText("")
        self.setting_btn.setText("")
        self.name_label.setText(QCoreApplication.translate("SerialItem", u"name", None))
        self.detal_label.setText(QCoreApplication.translate("SerialItem", u"detail", None))
    # retranslateUi

