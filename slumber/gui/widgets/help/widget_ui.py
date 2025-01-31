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
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName(u"horizontal_layout")
        self.horizontal_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontal_layout.setContentsMargins(-1, -1, -1, 16)
        self.back_button = QPushButton(HelpPage)
        self.back_button.setObjectName(u"back_button")
        self.back_button.setMinimumSize(QSize(50, 50))
        self.back_button.setMaximumSize(QSize(50, 50))
        self.back_button.setSizeIncrement(QSize(50, 50))
        self.back_button.setStyleSheet(u"QPushButton {\n"
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
        self.back_button.setIcon(icon)
        self.back_button.setIconSize(QSize(32, 32))

        self.horizontal_layout.addWidget(self.back_button)

        self.label = QLabel(HelpPage)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        self.label.setFont(font)

        self.horizontal_layout.addWidget(self.label)

        self.horizontal_spacer = QSpacerItem(40, 50, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontal_layout.addItem(self.horizontal_spacer)


        self.verticalLayout_3.addLayout(self.horizontal_layout)

        self.web_engine_view = QWebEngineView(HelpPage)
        self.web_engine_view.setObjectName(u"web_engine_view")
        sizePolicy.setHeightForWidth(self.web_engine_view.sizePolicy().hasHeightForWidth())
        self.web_engine_view.setSizePolicy(sizePolicy)
        self.web_engine_view.setMinimumSize(QSize(0, 0))
        self.web_engine_view.setMaximumSize(QSize(3840, 2160))

        self.verticalLayout_3.addWidget(self.web_engine_view)


        self.retranslateUi(HelpPage)

        QMetaObject.connectSlotsByName(HelpPage)
    # setupUi

    def retranslateUi(self, HelpPage):
        HelpPage.setWindowTitle(QCoreApplication.translate("HelpPage", u"Help", None))
        self.back_button.setText("")
        self.label.setText(QCoreApplication.translate("HelpPage", u"Help", None))
    # retranslateUi

