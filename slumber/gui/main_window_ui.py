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
        MainWindow.resize(1440, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMaximumSize(QSize(1920, 1080))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.header = QHBoxLayout()
        self.header.setSpacing(8)
        self.header.setObjectName(u"header")
        self.header.setContentsMargins(8, 8, 8, 8)
        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName(u"logo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(50)
        sizePolicy2.setVerticalStretch(50)
        sizePolicy2.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy2)
        self.logo.setMinimumSize(QSize(50, 50))
        self.logo.setMaximumSize(QSize(0, 16777215))
        self.logo.setSizeIncrement(QSize(50, 50))
        self.logo.setBaseSize(QSize(50, 50))
        self.logo.setPixmap(QPixmap(u"slumber/gui/resources/images/slumber_logo.svg"))
        self.logo.setScaledContents(True)

        self.header.addWidget(self.logo)

        self.logo_title = QLabel(self.centralwidget)
        self.logo_title.setObjectName(u"logo_title")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.logo_title.sizePolicy().hasHeightForWidth())
        self.logo_title.setSizePolicy(sizePolicy3)
        self.logo_title.setMinimumSize(QSize(200, 50))
        self.logo_title.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Arial Black"])
        font.setPointSize(36)
        font.setBold(True)
        self.logo_title.setFont(font)

        self.header.addWidget(self.logo_title)

        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header.addItem(self.horizontalSpacer)

        self.pushButton_help = QPushButton(self.centralwidget)
        self.pushButton_help.setObjectName(u"pushButton_help")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_help.sizePolicy().hasHeightForWidth())
        self.pushButton_help.setSizePolicy(sizePolicy4)
        self.pushButton_help.setMinimumSize(QSize(100, 35))
        self.pushButton_help.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(14)
        font1.setBold(False)
        font1.setItalic(False)
        self.pushButton_help.setFont(font1)
        self.pushButton_help.setStyleSheet(u"QPushButton {\n"
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
        self.pushButton_help.setIcon(icon)
        self.pushButton_help.setIconSize(QSize(20, 20))
        self.pushButton_help.setAutoDefault(False)
        self.pushButton_help.setFlat(False)

        self.header.addWidget(self.pushButton_help)

        self.pushButton_settings = QPushButton(self.centralwidget)
        self.pushButton_settings.setObjectName(u"pushButton_settings")
        sizePolicy4.setHeightForWidth(self.pushButton_settings.sizePolicy().hasHeightForWidth())
        self.pushButton_settings.setSizePolicy(sizePolicy4)
        self.pushButton_settings.setMinimumSize(QSize(100, 35))
        self.pushButton_settings.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_settings.setSizeIncrement(QSize(0, 0))
        self.pushButton_settings.setBaseSize(QSize(0, 0))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(14)
        self.pushButton_settings.setFont(font2)
        self.pushButton_settings.setStyleSheet(u"QPushButton {\n"
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
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SyncSynchronizing))
        self.pushButton_settings.setIcon(icon1)
        self.pushButton_settings.setIconSize(QSize(20, 20))

        self.header.addWidget(self.pushButton_settings)


        self.verticalLayout.addLayout(self.header)

        self.body = QVBoxLayout()
        self.body.setObjectName(u"body")
        self.body.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.body.setContentsMargins(0, 0, 0, 0)
        self.stackedWidgetPages = QStackedWidget(self.centralwidget)
        self.stackedWidgetPages.setObjectName(u"stackedWidgetPages")
        self.stackedWidgetPages.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.stackedWidgetPages.sizePolicy().hasHeightForWidth())
        self.stackedWidgetPages.setSizePolicy(sizePolicy1)
        self.stackedWidgetPages.setMaximumSize(QSize(16777215, 16777215))

        self.body.addWidget(self.stackedWidgetPages)


        self.verticalLayout.addLayout(self.body)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.pushButton_help.setDefault(False)
        self.stackedWidgetPages.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo.setText("")
        self.logo_title.setText(QCoreApplication.translate("MainWindow", u"SLUMBER", None))
        self.pushButton_help.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.pushButton_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

