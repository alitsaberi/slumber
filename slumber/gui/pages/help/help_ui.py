# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_HelpPage(object):
    def setupUi(self, HelpPage):
        if not HelpPage.objectName():
            HelpPage.setObjectName(u"HelpPage")
        HelpPage.setWindowModality(Qt.WindowModality.NonModal)
        HelpPage.resize(666, 566)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HelpPage.sizePolicy().hasHeightForWidth())
        HelpPage.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(HelpPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 16)
        self.help_back = QPushButton(HelpPage)
        self.help_back.setObjectName(u"help_back")
        self.help_back.setMinimumSize(QSize(50, 50))
        self.help_back.setMaximumSize(QSize(50, 50))
        self.help_back.setSizeIncrement(QSize(50, 50))
        self.help_back.setStyleSheet(u"QPushButton {\n"
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
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.help_back.setIcon(icon)
        self.help_back.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.help_back)

        self.label = QLabel(HelpPage)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_7 = QSpacerItem(40, 50, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.webEngineView_help = QWebEngineView(HelpPage)
        self.webEngineView_help.setObjectName(u"webEngineView_help")
        sizePolicy.setHeightForWidth(self.webEngineView_help.sizePolicy().hasHeightForWidth())
        self.webEngineView_help.setSizePolicy(sizePolicy)
        self.webEngineView_help.setMinimumSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.webEngineView_help)


        self.retranslateUi(HelpPage)

        QMetaObject.connectSlotsByName(HelpPage)
    # setupUi

    def retranslateUi(self, HelpPage):
        HelpPage.setWindowTitle(QCoreApplication.translate("HelpPage", u"Help", None))
        self.help_back.setText("")
        self.label.setText(QCoreApplication.translate("HelpPage", u"Help", None))
    # retranslateUi

