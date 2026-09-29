# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'serial_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFormLayout, QHBoxLayout,
    QLabel, QPlainTextEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSplitter, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_SerialPanel(object):
    def setupUi(self, SerialPanel):
        if not SerialPanel.objectName():
            SerialPanel.setObjectName(u"SerialPanel")
        SerialPanel.resize(606, 519)
        self.verticalLayout_3 = QVBoxLayout(SerialPanel)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.port_label = QLabel(SerialPanel)
        self.port_label.setObjectName(u"port_label")
        font = QFont()
        font.setPointSize(12)
        self.port_label.setFont(font)

        self.verticalLayout_3.addWidget(self.port_label)

        self.splitter = QSplitter(SerialPanel)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.textBrowser = QTextBrowser(self.splitter)
        self.textBrowser.setObjectName(u"textBrowser")
        self.splitter.addWidget(self.textBrowser)
        self.widget_5 = QWidget(self.splitter)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout = QVBoxLayout(self.widget_5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.widget_5)
        self.widget_3.setObjectName(u"widget_3")
        self.formLayout = QFormLayout(self.widget_3)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(9, 0, 9, 0)
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.widget = QWidget(self.widget_3)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.radio_btn_append_mode_none = QRadioButton(self.widget)
        self.radio_btn_group_append_mode = QButtonGroup(SerialPanel)
        self.radio_btn_group_append_mode.setObjectName(u"radio_btn_group_append_mode")
        self.radio_btn_group_append_mode.addButton(self.radio_btn_append_mode_none)
        self.radio_btn_append_mode_none.setObjectName(u"radio_btn_append_mode_none")

        self.horizontalLayout.addWidget(self.radio_btn_append_mode_none)

        self.radio_btn_append_mode_rn = QRadioButton(self.widget)
        self.radio_btn_group_append_mode.addButton(self.radio_btn_append_mode_rn)
        self.radio_btn_append_mode_rn.setObjectName(u"radio_btn_append_mode_rn")

        self.horizontalLayout.addWidget(self.radio_btn_append_mode_rn)

        self.radio_btn_append_mode_r = QRadioButton(self.widget)
        self.radio_btn_group_append_mode.addButton(self.radio_btn_append_mode_r)
        self.radio_btn_append_mode_r.setObjectName(u"radio_btn_append_mode_r")

        self.horizontalLayout.addWidget(self.radio_btn_append_mode_r)

        self.radio_btn_append_mode_n = QRadioButton(self.widget)
        self.radio_btn_group_append_mode.addButton(self.radio_btn_append_mode_n)
        self.radio_btn_append_mode_n.setObjectName(u"radio_btn_append_mode_n")

        self.horizontalLayout.addWidget(self.radio_btn_append_mode_n)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.widget)

        self.widget_2 = QWidget(self.widget_3)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.radio_btn_send_mode_str = QRadioButton(self.widget_2)
        self.radio_btn_group_send_mode = QButtonGroup(SerialPanel)
        self.radio_btn_group_send_mode.setObjectName(u"radio_btn_group_send_mode")
        self.radio_btn_group_send_mode.addButton(self.radio_btn_send_mode_str)
        self.radio_btn_send_mode_str.setObjectName(u"radio_btn_send_mode_str")

        self.horizontalLayout_2.addWidget(self.radio_btn_send_mode_str)

        self.radio_btn_send_mode_hex = QRadioButton(self.widget_2)
        self.radio_btn_group_send_mode.addButton(self.radio_btn_send_mode_hex)
        self.radio_btn_send_mode_hex.setObjectName(u"radio_btn_send_mode_hex")

        self.horizontalLayout_2.addWidget(self.radio_btn_send_mode_hex)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.widget_2)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_5)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.input = QPlainTextEdit(self.widget_4)
        self.input.setObjectName(u"input")

        self.horizontalLayout_3.addWidget(self.input)

        self.send_btn = QPushButton(self.widget_4)
        self.send_btn.setObjectName(u"send_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.send_btn.sizePolicy().hasHeightForWidth())
        self.send_btn.setSizePolicy(sizePolicy)
        self.send_btn.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_3.addWidget(self.send_btn)


        self.verticalLayout.addWidget(self.widget_4)

        self.splitter.addWidget(self.widget_5)

        self.verticalLayout_3.addWidget(self.splitter)


        self.retranslateUi(SerialPanel)

        QMetaObject.connectSlotsByName(SerialPanel)
    # setupUi

    def retranslateUi(self, SerialPanel):
        SerialPanel.setWindowTitle(QCoreApplication.translate("SerialPanel", u"Form", None))
        self.port_label.setText(QCoreApplication.translate("SerialPanel", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("SerialPanel", u"\u5c3e\u90e8\u8ffd\u52a0", None))
        self.label_2.setText(QCoreApplication.translate("SerialPanel", u"\u53d1\u9001\u6a21\u5f0f", None))
        self.radio_btn_append_mode_none.setText(QCoreApplication.translate("SerialPanel", u"\u4e0d\u8ffd\u52a0", None))
        self.radio_btn_append_mode_rn.setText(QCoreApplication.translate("SerialPanel", u"\\r\\n", None))
        self.radio_btn_append_mode_r.setText(QCoreApplication.translate("SerialPanel", u"\\r", None))
        self.radio_btn_append_mode_n.setText(QCoreApplication.translate("SerialPanel", u"\\n", None))
        self.radio_btn_send_mode_str.setText(QCoreApplication.translate("SerialPanel", u"str", None))
        self.radio_btn_send_mode_hex.setText(QCoreApplication.translate("SerialPanel", u"hex", None))
        self.send_btn.setText("")
    # retranslateUi

