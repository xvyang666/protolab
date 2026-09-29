# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'serial_item_setting.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_SerialItemSetting(object):
    def setupUi(self, SerialItemSetting):
        if not SerialItemSetting.objectName():
            SerialItemSetting.setObjectName(u"SerialItemSetting")
        SerialItemSetting.resize(329, 239)
        self.verticalLayout = QVBoxLayout(SerialItemSetting)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.port_name_label = QLabel(SerialItemSetting)
        self.port_name_label.setObjectName(u"port_name_label")
        font = QFont()
        font.setPointSize(16)
        self.port_name_label.setFont(font)

        self.verticalLayout.addWidget(self.port_name_label)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(SerialItemSetting)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.label_3 = QLabel(SerialItemSetting)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.label_4 = QLabel(SerialItemSetting)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.baud_rate_select = QComboBox(SerialItemSetting)
        self.baud_rate_select.setObjectName(u"baud_rate_select")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.baud_rate_select)

        self.data_bit_select = QComboBox(SerialItemSetting)
        self.data_bit_select.setObjectName(u"data_bit_select")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.data_bit_select)

        self.parity_select = QComboBox(SerialItemSetting)
        self.parity_select.setObjectName(u"parity_select")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.parity_select)

        self.label_5 = QLabel(SerialItemSetting)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.stop_bit_select = QComboBox(SerialItemSetting)
        self.stop_bit_select.setObjectName(u"stop_bit_select")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.stop_bit_select)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(SerialItemSetting)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SerialItemSetting)
        self.buttonBox.accepted.connect(SerialItemSetting.accept)
        self.buttonBox.rejected.connect(SerialItemSetting.reject)

        QMetaObject.connectSlotsByName(SerialItemSetting)
    # setupUi

    def retranslateUi(self, SerialItemSetting):
        SerialItemSetting.setWindowTitle(QCoreApplication.translate("SerialItemSetting", u"Dialog", None))
        self.port_name_label.setText(QCoreApplication.translate("SerialItemSetting", u"com0", None))
        self.label_2.setText(QCoreApplication.translate("SerialItemSetting", u"\u6ce2\u7279\u7387", None))
        self.label_3.setText(QCoreApplication.translate("SerialItemSetting", u"\u6570\u636e\u4f4d", None))
        self.label_4.setText(QCoreApplication.translate("SerialItemSetting", u"\u6821\u9a8c\u4f4d", None))
        self.label_5.setText(QCoreApplication.translate("SerialItemSetting", u"\u505c\u6b62\u4f4d", None))
    # retranslateUi

