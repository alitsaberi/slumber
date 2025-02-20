# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLCDNumber, QLabel,
    QLayout, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ZMaxConnectionPage(object):
    def setupUi(self, ZMaxConnectionPage):
        if not ZMaxConnectionPage.objectName():
            ZMaxConnectionPage.setObjectName(u"ZMaxConnectionPage")
        ZMaxConnectionPage.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ZMaxConnectionPage.sizePolicy().hasHeightForWidth())
        ZMaxConnectionPage.setSizePolicy(sizePolicy)
        ZMaxConnectionPage.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout = QVBoxLayout(ZMaxConnectionPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header = QHBoxLayout()
        self.header.setObjectName(u"header")
        self.header.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.title = QLabel(ZMaxConnectionPage)
        self.title.setObjectName(u"title")
        self.title.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        self.title.setFont(font)

        self.header.addWidget(self.title)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header.addItem(self.horizontal_spacer)

        self.info_button = QPushButton(ZMaxConnectionPage)
        self.info_button.setObjectName(u"info_button")
        self.info_button.setMinimumSize(QSize(50, 50))
        self.info_button.setMaximumSize(QSize(50, 50))
        self.info_button.setStyleSheet(u"QPushButton {\n"
"                                    color: rgb(255, 255, 255);\n"
"                                    background-color: rgb(1, 92, 187);\n"
"                                    border: 1px;\n"
"                                    border-radius: 10px;\n"
"                                    }\n"
"\n"
"                                    QPushButton:hover {\n"
"                                    color: rgb(220,221,229);\n"
"                                    background-color: rgb(37, 150, 190);\n"
"                                    }\n"
"\n"
"                                    QPushButton:pressed {\n"
"                                    color: rgb(220,221,229);\n"
"                                    background-color: rgb(37, 150, 190);\n"
"                                    }")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogInformation))
        self.info_button.setIcon(icon)
        self.info_button.setIconSize(QSize(40, 40))

        self.header.addWidget(self.info_button)


        self.verticalLayout.addLayout(self.header)

        self.body = QVBoxLayout()
        self.body.setObjectName(u"body")
        self.body.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.body.addItem(self.verticalSpacer)

        self.connect_button = QPushButton(ZMaxConnectionPage)
        self.connect_button.setObjectName(u"connect_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.connect_button.sizePolicy().hasHeightForWidth())
        self.connect_button.setSizePolicy(sizePolicy1)
        self.connect_button.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4CAF50, stop:1 #2E7D32);\n"
"                color: white;\n"
"                font-weight: bold;\n"
"                padding: 10px;\n"
"                border-radius: 5px;")

        self.body.addWidget(self.connect_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.battery_layout = QHBoxLayout()
        self.battery_layout.setSpacing(0)
        self.battery_layout.setObjectName(u"battery_layout")
        self.battery_layout.setContentsMargins(-1, 50, -1, 25)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.battery_layout.addItem(self.horizontalSpacer)

        self.battery_label = QLabel(ZMaxConnectionPage)
        self.battery_label.setObjectName(u"battery_label")
        sizePolicy1.setHeightForWidth(self.battery_label.sizePolicy().hasHeightForWidth())
        self.battery_label.setSizePolicy(sizePolicy1)
        self.battery_label.setMinimumSize(QSize(100, 50))
        self.battery_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.battery_label.setStyleSheet(u"color: white;")

        self.battery_layout.addWidget(self.battery_label)

        self.battery_led = QLCDNumber(ZMaxConnectionPage)
        self.battery_led.setObjectName(u"battery_led")
        sizePolicy1.setHeightForWidth(self.battery_led.sizePolicy().hasHeightForWidth())
        self.battery_led.setSizePolicy(sizePolicy1)
        self.battery_led.setMinimumSize(QSize(100, 50))

        self.battery_layout.addWidget(self.battery_led)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.battery_layout.addItem(self.horizontalSpacer_2)


        self.body.addLayout(self.battery_layout)

        self.status_label = QLabel(ZMaxConnectionPage)
        self.status_label.setObjectName(u"status_label")
        sizePolicy1.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        self.status_label.setFont(font1)
        self.status_label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.1);\n"
"            color: white;\n"
"            padding: 10px;\n"
"            border-radius: 10px;")

        self.body.addWidget(self.status_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.body.addItem(self.verticalSpacer_2)

        self.body.setStretch(1, 2)
        self.body.setStretch(3, 2)

        self.verticalLayout.addLayout(self.body)


        self.retranslateUi(ZMaxConnectionPage)

        QMetaObject.connectSlotsByName(ZMaxConnectionPage)
    # setupUi

    def retranslateUi(self, ZMaxConnectionPage):
        ZMaxConnectionPage.setWindowTitle(QCoreApplication.translate("ZMaxConnectionPage", u"{{ header}}", None))
        self.title.setText(QCoreApplication.translate("ZMaxConnectionPage", u"{{ header }}", None))
        self.info_button.setText("")
        self.connect_button.setText(QCoreApplication.translate("ZMaxConnectionPage", u"Connect", None))
        self.battery_label.setText(QCoreApplication.translate("ZMaxConnectionPage", u"Battery Lavel:", None))
        self.status_label.setText(QCoreApplication.translate("ZMaxConnectionPage", u"Please click \"Connect\" to connect to the EEG server.", None))
    # retranslateUi

