# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.NonModal)
        MainWindow.resize(1060, 762)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMaximumSize(QSize(3840, 2160))
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.central_widget.setMaximumSize(QSize(3840, 2160))
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget = QStackedWidget(self.central_widget)
        self.stacked_widget.setObjectName(u"stacked_widget")
        self.main_page = QWidget()
        self.main_page.setObjectName(u"main_page")
        self.vertical_layout = QVBoxLayout(self.main_page)
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.vertical_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.header = QHBoxLayout()
        self.header.setSpacing(8)
        self.header.setObjectName(u"header")
        self.header.setContentsMargins(8, 8, 8, 8)
        self.logo = QLabel(self.main_page)
        self.logo.setObjectName(u"logo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(50)
        sizePolicy1.setVerticalStretch(50)
        sizePolicy1.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy1)
        self.logo.setMinimumSize(QSize(50, 50))
        self.logo.setMaximumSize(QSize(0, 16777215))
        self.logo.setSizeIncrement(QSize(50, 50))
        self.logo.setBaseSize(QSize(50, 50))
        self.logo.setPixmap(QPixmap(u"resources/images/slumber_logo.svg"))
        self.logo.setScaledContents(True)

        self.header.addWidget(self.logo)

        self.logo_title = QLabel(self.main_page)
        self.logo_title.setObjectName(u"logo_title")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.logo_title.sizePolicy().hasHeightForWidth())
        self.logo_title.setSizePolicy(sizePolicy2)
        self.logo_title.setMinimumSize(QSize(200, 50))
        self.logo_title.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Arial Black"])
        font.setPointSize(36)
        font.setBold(True)
        self.logo_title.setFont(font)

        self.header.addWidget(self.logo_title)

        self.horizontal_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header.addItem(self.horizontal_spacer)

        self.help_button = QPushButton(self.main_page)
        self.help_button.setObjectName(u"help_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.help_button.sizePolicy().hasHeightForWidth())
        self.help_button.setSizePolicy(sizePolicy3)
        self.help_button.setMinimumSize(QSize(100, 35))
        self.help_button.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        font1.setBold(False)
        font1.setItalic(False)
        self.help_button.setFont(font1)
        self.help_button.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(1, 92, 187);\n"
"	border: 1px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	color: rgb(220,221,229);\n"
"	background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	color: rgb(220,221,229);\n"
"	background-color: rgb(37, 150, 190);\n"
"}")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpFaq))
        self.help_button.setIcon(icon)
        self.help_button.setIconSize(QSize(20, 20))
        self.help_button.setAutoDefault(False)
        self.help_button.setFlat(False)

        self.header.addWidget(self.help_button)

        self.settings_button = QPushButton(self.main_page)
        self.settings_button.setObjectName(u"settings_button")
        sizePolicy3.setHeightForWidth(self.settings_button.sizePolicy().hasHeightForWidth())
        self.settings_button.setSizePolicy(sizePolicy3)
        self.settings_button.setMinimumSize(QSize(100, 35))
        self.settings_button.setMaximumSize(QSize(16777215, 16777215))
        self.settings_button.setSizeIncrement(QSize(0, 0))
        self.settings_button.setBaseSize(QSize(0, 0))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(14)
        self.settings_button.setFont(font2)
        self.settings_button.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(1, 92, 187);\n"
"	border: 1px;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	color: rgb(220,221,229);\n"
"	background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	color: rgb(220,221,229);\n"
"	background-color: rgb(37, 150, 190);\n"
"}")
        self.settings_button.setIconSize(QSize(20, 20))

        self.header.addWidget(self.settings_button)


        self.vertical_layout.addLayout(self.header)

        self.body = QVBoxLayout()
        self.body.setObjectName(u"body")
        self.body.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body_stacked_widget = QStackedWidget(self.main_page)
        self.body_stacked_widget.setObjectName(u"body_stacked_widget")
        self.body_stacked_widget.setEnabled(True)
        sizePolicy.setHeightForWidth(self.body_stacked_widget.sizePolicy().hasHeightForWidth())
        self.body_stacked_widget.setSizePolicy(sizePolicy)
        self.body_stacked_widget.setMaximumSize(QSize(3840, 2160))

        self.body.addWidget(self.body_stacked_widget)


        self.vertical_layout.addLayout(self.body)

        self.stacked_widget.addWidget(self.main_page)

        self.gridLayout.addWidget(self.stacked_widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)

        self.help_button.setDefault(False)
        self.body_stacked_widget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SLUMBER", None))
        self.logo.setText("")
        self.logo_title.setText(QCoreApplication.translate("MainWindow", u"SLUMBER", None))
        self.help_button.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_button.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

