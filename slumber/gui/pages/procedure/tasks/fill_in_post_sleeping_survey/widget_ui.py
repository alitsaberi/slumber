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

        self.webEngineView_post_survey = QWebEngineView(Widget)
        self.webEngineView_post_survey.setObjectName(u"webEngineView_post_survey")
        sizePolicy.setHeightForWidth(self.webEngineView_post_survey.sizePolicy().hasHeightForWidth())
        self.webEngineView_post_survey.setSizePolicy(sizePolicy)
        self.webEngineView_post_survey.setMinimumSize(QSize(0, 0))
        self.webEngineView_post_survey.setMaximumSize(QSize(3840, 2160))

        self.verticalLayout.addWidget(self.webEngineView_post_survey)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Fill in Post-Sleeping Survey", None))
        self.widget_title.setText(QCoreApplication.translate("Widget", u"Fill in Post-Sleeping Survey", None))
        self.button_info.setText("")
    # retranslateUi

