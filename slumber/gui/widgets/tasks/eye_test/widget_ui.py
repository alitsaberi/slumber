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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_EyeTestPage(object):
    def setupUi(self, EyeTestPage):
        if not EyeTestPage.objectName():
            EyeTestPage.setObjectName(u"EyeTestPage")
        EyeTestPage.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EyeTestPage.sizePolicy().hasHeightForWidth())
        EyeTestPage.setSizePolicy(sizePolicy)
        EyeTestPage.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout = QVBoxLayout(EyeTestPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header = QHBoxLayout()
        self.header.setObjectName(u"header")
        self.header.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.title = QLabel(EyeTestPage)
        self.title.setObjectName(u"title")
        self.title.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        self.title.setFont(font)

        self.header.addWidget(self.title)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header.addItem(self.horizontal_spacer)

        self.info_button = QPushButton(EyeTestPage)
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

        self.test_button = QPushButton(EyeTestPage)
        self.test_button.setObjectName(u"test_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.test_button.sizePolicy().hasHeightForWidth())
        self.test_button.setSizePolicy(sizePolicy1)
        self.test_button.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4CAF50, stop:1 #2E7D32);\n"
"                color: white;\n"
"                font-weight: bold;\n"
"                padding: 10px;\n"
"                border-radius: 5px;")

        self.body.addWidget(self.test_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.status_label = QLabel(EyeTestPage)
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
        self.status_label.setMargin(0)

        self.body.addWidget(self.status_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.body.addItem(self.verticalSpacer_2)

        self.body.setStretch(1, 2)
        self.body.setStretch(2, 2)

        self.verticalLayout.addLayout(self.body)


        self.retranslateUi(EyeTestPage)

        QMetaObject.connectSlotsByName(EyeTestPage)
    # setupUi

    def retranslateUi(self, EyeTestPage):
        EyeTestPage.setWindowTitle(QCoreApplication.translate("EyeTestPage", u"{{ header}}", None))
        self.title.setText(QCoreApplication.translate("EyeTestPage", u"{{ header }}", None))
        self.info_button.setText("")
        self.test_button.setText(QCoreApplication.translate("EyeTestPage", u"Start", None))
        self.status_label.setText(QCoreApplication.translate("EyeTestPage", u"Please click \"Start\" to start the test.", None))
    # retranslateUi

