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

class Ui_EmptyPage(object):
    def setupUi(self, EmptyPage):
        if not EmptyPage.objectName():
            EmptyPage.setObjectName(u"EmptyPage")
        EmptyPage.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EmptyPage.sizePolicy().hasHeightForWidth())
        EmptyPage.setSizePolicy(sizePolicy)
        EmptyPage.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout = QVBoxLayout(EmptyPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header = QHBoxLayout()
        self.header.setObjectName(u"header")
        self.header.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.title = QLabel(EmptyPage)
        self.title.setObjectName(u"title")
        self.title.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        self.title.setFont(font)

        self.header.addWidget(self.title)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header.addItem(self.horizontal_spacer)

        self.info_button = QPushButton(EmptyPage)
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
        self.done_button = QPushButton(EmptyPage)
        self.done_button.setObjectName(u"done_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.done_button.sizePolicy().hasHeightForWidth())
        self.done_button.setSizePolicy(sizePolicy1)

        self.body.addWidget(self.done_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.body.setStretch(0, 1)

        self.verticalLayout.addLayout(self.body)


        self.retranslateUi(EmptyPage)

        QMetaObject.connectSlotsByName(EmptyPage)
    # setupUi

    def retranslateUi(self, EmptyPage):
        EmptyPage.setWindowTitle(QCoreApplication.translate("EmptyPage", u"{{ header}}", None))
        self.title.setText(QCoreApplication.translate("EmptyPage", u"{{ header }}", None))
        self.info_button.setText("")
        self.done_button.setText(QCoreApplication.translate("EmptyPage", u"Done", None))
    # retranslateUi

