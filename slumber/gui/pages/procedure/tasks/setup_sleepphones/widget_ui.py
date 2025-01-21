# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QListWidget, QListWidgetItem, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.widget_title = QLabel(Widget)
        self.widget_title.setObjectName(u"widget_title")
        self.widget_title.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        self.widget_title.setFont(font)

        self.horizontalLayout_4.addWidget(self.widget_title)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.button_info = QPushButton(Widget)
        self.button_info.setObjectName(u"button_info")
        self.button_info.setMinimumSize(QSize(50, 50))
        self.button_info.setMaximumSize(QSize(50, 50))
        self.button_info.setStyleSheet(u"QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(1, 92, 187);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogInformation))
        self.button_info.setIcon(icon)
        self.button_info.setIconSize(QSize(40, 40))

        self.horizontalLayout_4.addWidget(self.button_info)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.webEngineView_sleep_phones = QWebEngineView(Widget)
        self.webEngineView_sleep_phones.setObjectName(u"webEngineView_sleep_phones")
        sizePolicy.setHeightForWidth(self.webEngineView_sleep_phones.sizePolicy().hasHeightForWidth())
        self.webEngineView_sleep_phones.setSizePolicy(sizePolicy)
        self.webEngineView_sleep_phones.setMinimumSize(QSize(0, 0))
        self.webEngineView_sleep_phones.setMaximumSize(QSize(3840, 2160))

        self.verticalLayout.addWidget(self.webEngineView_sleep_phones)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(18)
        self.label.setFont(font1)

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.radio_status = QRadioButton(Widget)
        self.radio_status.setObjectName(u"radio_status")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(14)
        self.radio_status.setFont(font2)
        self.radio_status.setCheckable(False)

        self.horizontalLayout.addWidget(self.radio_status)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.button_refresh = QPushButton(Widget)
        self.button_refresh.setObjectName(u"button_refresh")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_refresh.sizePolicy().hasHeightForWidth())
        self.button_refresh.setSizePolicy(sizePolicy1)
        self.button_refresh.setMinimumSize(QSize(100, 30))
        self.button_refresh.setStyleSheet(u"QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(1, 92, 187);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"  color: rgb(190, 190, 190);\n"
"  background-color: rgb(100, 100, 100);\n"
"}")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.button_refresh.setIcon(icon1)

        self.horizontalLayout.addWidget(self.button_refresh)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.list_bluetooth_devices = QListWidget(Widget)
        QListWidgetItem(self.list_bluetooth_devices)
        self.list_bluetooth_devices.setObjectName(u"list_bluetooth_devices")

        self.verticalLayout_3.addWidget(self.list_bluetooth_devices)


        self.verticalLayout.addLayout(self.verticalLayout_3)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Setup SleepPhones", None))
        self.widget_title.setText(QCoreApplication.translate("Widget", u"Setup SleepPhones", None))
        self.button_info.setText("")
        self.label.setText(QCoreApplication.translate("Widget", u"Bluetooth Devices", None))
        self.radio_status.setText(QCoreApplication.translate("Widget", u"Status", None))
        self.button_refresh.setText(QCoreApplication.translate("Widget", u"Refresh", None))

        __sortingEnabled = self.list_bluetooth_devices.isSortingEnabled()
        self.list_bluetooth_devices.setSortingEnabled(False)
        ___qlistwidgetitem = self.list_bluetooth_devices.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Widget", u"Loading...", None));
        self.list_bluetooth_devices.setSortingEnabled(__sortingEnabled)

    # retranslateUi

