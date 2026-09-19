# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Setting(object):
    def setupUi(self, Setting):
        if not Setting.objectName():
            Setting.setObjectName(u"Setting")
        Setting.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Setting)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(Setting)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 378, 278))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Microsoft YaHei Light"])
        font.setPointSize(24)
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_3.setFont(font1)

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.style_select = QComboBox(self.frame)
        self.style_select.setObjectName(u"style_select")

        self.gridLayout.addWidget(self.style_select, 0, 2, 2, 1)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        font2 = QFont()
        font2.setPointSize(8)
        self.label_5.setFont(font2)

        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1)

        self.style_icon = QLabel(self.frame)
        self.style_icon.setObjectName(u"style_icon")

        self.gridLayout.addWidget(self.style_icon, 0, 0, 2, 1)

        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnMinimumWidth(0, 50)

        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.scrollAreaWidgetContents)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(4)
        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.gridLayout_2.addWidget(self.label_6, 0, 1, 1, 1)

        self.theme_select = QComboBox(self.frame_2)
        self.theme_select.setObjectName(u"theme_select")

        self.gridLayout_2.addWidget(self.theme_select, 0, 2, 2, 1)

        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font2)

        self.gridLayout_2.addWidget(self.label_7, 1, 1, 1, 1)

        self.theme_icon = QLabel(self.frame_2)
        self.theme_icon.setObjectName(u"theme_icon")

        self.gridLayout_2.addWidget(self.theme_icon, 0, 0, 2, 1)

        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnMinimumWidth(0, 50)

        self.verticalLayout_2.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Setting)

        QMetaObject.connectSlotsByName(Setting)
    # setupUi

    def retranslateUi(self, Setting):
        Setting.setWindowTitle(QCoreApplication.translate("Setting", u"Form", None))
        self.label.setText(QCoreApplication.translate("Setting", u"\u8bbe\u7f6e", None))
        self.label_2.setText(QCoreApplication.translate("Setting", u"\u5916\u89c2", None))
        self.label_3.setText(QCoreApplication.translate("Setting", u"\u63a7\u4ef6\u6837\u5f0f", None))
        self.label_5.setText(QCoreApplication.translate("Setting", u"\u9009\u62e9\u754c\u9762\u7684\u5916\u89c2", None))
        self.style_icon.setText(QCoreApplication.translate("Setting", u"icon", None))
        self.label_6.setText(QCoreApplication.translate("Setting", u"\u5e94\u7528\u4e3b\u9898", None))
        self.label_7.setText(QCoreApplication.translate("Setting", u"\u9009\u62e9\u6df1\u6d45\u989c\u8272\u4e3b\u9898", None))
        self.theme_icon.setText(QCoreApplication.translate("Setting", u"icon", None))
    # retranslateUi

