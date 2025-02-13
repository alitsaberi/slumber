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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_SleepPage(object):
    def setupUi(self, SleepPage):
        if not SleepPage.objectName():
            SleepPage.setObjectName(u"SleepPage")
        SleepPage.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SleepPage.sizePolicy().hasHeightForWidth())
        SleepPage.setSizePolicy(sizePolicy)
        SleepPage.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout = QVBoxLayout(SleepPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.body = QVBoxLayout()
        self.body.setObjectName(u"body")
        self.body.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.body.addItem(self.verticalSpacer)

        self.status_layout = QHBoxLayout()
        self.status_layout.setObjectName(u"status_layout")
        self.status_layout.setContentsMargins(-1, 0, -1, 20)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.status_layout.addItem(self.horizontalSpacer)

        self.status_help_label = QLabel(SleepPage)
        self.status_help_label.setObjectName(u"status_help_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.status_help_label.sizePolicy().hasHeightForWidth())
        self.status_help_label.setSizePolicy(sizePolicy1)
        self.status_help_label.setStyleSheet(u"color: white;")

        self.status_layout.addWidget(self.status_help_label)

        self.status_label = QLabel(SleepPage)
        self.status_label.setObjectName(u"status_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        self.status_label.setFont(font)
        self.status_label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.1);\n"
"            color: white;\n"
"            padding: 10px;\n"
"            border-radius: 10px;")

        self.status_layout.addWidget(self.status_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.status_layout.addItem(self.horizontalSpacer_2)


        self.body.addLayout(self.status_layout)

        self.awake_button = QPushButton(SleepPage)
        self.awake_button.setObjectName(u"awake_button")
        sizePolicy2.setHeightForWidth(self.awake_button.sizePolicy().hasHeightForWidth())
        self.awake_button.setSizePolicy(sizePolicy2)
        self.awake_button.setStyleSheet(u"QPushButton {\n"
"                font-size: 18px;\n"
"                padding: 12px;\n"
"                border-radius: 10px;\n"
"                border: 2px solid #88C0D0;\n"
"                background-color: #5E81AC;\n"
"                color: white;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #81A1C1;\n"
"            }\n"
"            QPushButton:disabled {\n"
"                background-color: #4C566A;\n"
"                border: 2px solid #3B4252;\n"
"                color: #D8DEE9;\n"
"            }")

        self.body.addWidget(self.awake_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.sleep_button = QPushButton(SleepPage)
        self.sleep_button.setObjectName(u"sleep_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sleep_button.sizePolicy().hasHeightForWidth())
        self.sleep_button.setSizePolicy(sizePolicy3)
        self.sleep_button.setStyleSheet(u"QPushButton {\n"
"                font-size: 18px;\n"
"                padding: 12px;\n"
"                border-radius: 10px;\n"
"                border: 2px solid #88C0D0;\n"
"                background-color: #5E81AC;\n"
"                color: white;\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #81A1C1;\n"
"            }\n"
"            QPushButton:disabled {\n"
"                background-color: #4C566A;\n"
"                border: 2px solid #3B4252;\n"
"                color: #D8DEE9;\n"
"            }")

        self.body.addWidget(self.sleep_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.body.addItem(self.verticalSpacer_2)

        self.end_button = QPushButton(SleepPage)
        self.end_button.setObjectName(u"end_button")
        sizePolicy2.setHeightForWidth(self.end_button.sizePolicy().hasHeightForWidth())
        self.end_button.setSizePolicy(sizePolicy2)
        self.end_button.setStyleSheet(u"QPushButton {\n"
"    font-size: 18px;\n"
"    padding: 12px;\n"
"    border-radius: 10px;\n"
"    border: 2px solid #E67E22;\n"
"    background-color: #D35400;\n"
"    color: white;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #E98B39;\n"
"}\n"
"QPushButton:disabled {\n"
"    background-color: #A04000;\n"
"    border: 2px solid #873600;\n"
"    color: #FDEBD0;\n"
"}\n"
"")

        self.body.addWidget(self.end_button, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout.addLayout(self.body)


        self.retranslateUi(SleepPage)

        QMetaObject.connectSlotsByName(SleepPage)
    # setupUi

    def retranslateUi(self, SleepPage):
        SleepPage.setWindowTitle(QCoreApplication.translate("SleepPage", u"{{ header}}", None))
        self.status_help_label.setText(QCoreApplication.translate("SleepPage", u"Current Status:", None))
        self.status_label.setText("")
        self.awake_button.setText(QCoreApplication.translate("SleepPage", u"Awake", None))
        self.sleep_button.setText(QCoreApplication.translate("SleepPage", u"Going to Sleep", None))
        self.end_button.setText(QCoreApplication.translate("SleepPage", u"End Session", None))
    # retranslateUi

