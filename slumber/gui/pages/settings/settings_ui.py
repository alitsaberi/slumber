# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLCDNumber,
    QLabel, QLayout, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.setWindowModality(Qt.WindowModality.NonModal)
        SettingsWindow.resize(1158, 973)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsWindow.sizePolicy().hasHeightForWidth())
        SettingsWindow.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(SettingsWindow)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_title = QHBoxLayout()
        self.horizontalLayout_title.setObjectName(u"horizontalLayout_title")
        self.horizontalLayout_title.setContentsMargins(-1, -1, -1, 16)
        self.settings_back = QPushButton(SettingsWindow)
        self.settings_back.setObjectName(u"settings_back")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.settings_back.sizePolicy().hasHeightForWidth())
        self.settings_back.setSizePolicy(sizePolicy1)
        self.settings_back.setMinimumSize(QSize(50, 50))
        self.settings_back.setMaximumSize(QSize(50, 50))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(18)
        self.settings_back.setFont(font)
        self.settings_back.setStyleSheet(u"QPushButton {\n"
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
        self.settings_back.setIcon(icon)
        self.settings_back.setIconSize(QSize(32, 32))

        self.horizontalLayout_title.addWidget(self.settings_back)

        self.label_6 = QLabel(SettingsWindow)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(36)
        self.label_6.setFont(font1)

        self.horizontalLayout_title.addWidget(self.label_6)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_title.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout_title)

        self.card_font_size = QWidget(SettingsWindow)
        self.card_font_size.setObjectName(u"card_font_size")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.card_font_size.sizePolicy().hasHeightForWidth())
        self.card_font_size.setSizePolicy(sizePolicy2)
        self.card_font_size.setMinimumSize(QSize(0, 100))
        self.card_font_size.setStyleSheet(u"QWidget {\n"
"    border: 2px solid rgb(50, 50, 50);\n"
"    border-radius: 10px;\n"
"    background-color: rgb(30, 30, 30);\n"
"    padding: 10px\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.card_font_size)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(self.card_font_size)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setMinimumSize(QSize(0, 50))
        self.label_5.setFont(font)
        self.label_5.setAutoFillBackground(False)

        self.verticalLayout_2.addWidget(self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 8, -1, 8)
        self.pushButton_font_size_dec = QPushButton(self.card_font_size)
        self.pushButton_font_size_dec.setObjectName(u"pushButton_font_size_dec")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(50)
        sizePolicy4.setVerticalStretch(50)
        sizePolicy4.setHeightForWidth(self.pushButton_font_size_dec.sizePolicy().hasHeightForWidth())
        self.pushButton_font_size_dec.setSizePolicy(sizePolicy4)
        self.pushButton_font_size_dec.setMinimumSize(QSize(50, 50))
        self.pushButton_font_size_dec.setMaximumSize(QSize(50, 50))
        self.pushButton_font_size_dec.setStyleSheet(u"QPushButton {\n"
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
"QPushButton:hover {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(190, 190, 190);\n"
"    background-color: rgb(100, 100, 100);\n"
"}\n"
"QPushButton:pressed {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}")
        self.pushButton_font_size_dec.setText(u"")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListRemove))
        self.pushButton_font_size_dec.setIcon(icon1)
        self.pushButton_font_size_dec.setIconSize(QSize(30, 40))

        self.horizontalLayout_2.addWidget(self.pushButton_font_size_dec)

        self.lcdNumber_font_size = QLCDNumber(self.card_font_size)
        self.lcdNumber_font_size.setObjectName(u"lcdNumber_font_size")
        sizePolicy1.setHeightForWidth(self.lcdNumber_font_size.sizePolicy().hasHeightForWidth())
        self.lcdNumber_font_size.setSizePolicy(sizePolicy1)
        self.lcdNumber_font_size.setMinimumSize(QSize(300, 50))
        self.lcdNumber_font_size.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.lcdNumber_font_size)

        self.pushButton_font_size_add = QPushButton(self.card_font_size)
        self.pushButton_font_size_add.setObjectName(u"pushButton_font_size_add")
        sizePolicy4.setHeightForWidth(self.pushButton_font_size_add.sizePolicy().hasHeightForWidth())
        self.pushButton_font_size_add.setSizePolicy(sizePolicy4)
        self.pushButton_font_size_add.setMinimumSize(QSize(50, 50))
        self.pushButton_font_size_add.setMaximumSize(QSize(50, 50))
        self.pushButton_font_size_add.setStyleSheet(u"QPushButton {\n"
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
"QPushButton:hover {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(190, 190, 190);\n"
"    background-color: rgb(100, 100, 100);\n"
"}\n"
"QPushButton:pressed {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}")
        self.pushButton_font_size_add.setText(u"")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.pushButton_font_size_add.setIcon(icon2)
        self.pushButton_font_size_add.setIconSize(QSize(30, 40))

        self.horizontalLayout_2.addWidget(self.pushButton_font_size_add)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_6.addWidget(self.card_font_size)

        self.widget = QWidget(SettingsWindow)
        self.widget.setObjectName(u"widget")
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)
        self.widget.setStyleSheet(u"QWidget {\n"
"    border: 2px solid rgb(50, 50, 50);\n"
"    border-radius: 10px;\n"
"    background-color: rgb(30, 30, 30);\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QComboBox {\n"
"    border-radius: 0px; \n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)
        self.label_8.setMinimumSize(QSize(0, 50))
        self.label_8.setFont(font)

        self.verticalLayout_3.addWidget(self.label_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(-1, 8, -1, 8)
        self.comboBox_size = QComboBox(self.widget)
        self.comboBox_size.addItem("")
        self.comboBox_size.addItem("")
        self.comboBox_size.addItem("")
        self.comboBox_size.addItem("")
        self.comboBox_size.addItem("")
        self.comboBox_size.addItem("")
        self.comboBox_size.addItem("")
        self.comboBox_size.addItem("")
        self.comboBox_size.setObjectName(u"comboBox_size")
        sizePolicy1.setHeightForWidth(self.comboBox_size.sizePolicy().hasHeightForWidth())
        self.comboBox_size.setSizePolicy(sizePolicy1)
        self.comboBox_size.setMinimumSize(QSize(300, 0))
        font2 = QFont()
        font2.setPointSize(18)
        self.comboBox_size.setFont(font2)

        self.horizontalLayout_3.addWidget(self.comboBox_size)

        self.comboBox_window_mode = QComboBox(self.widget)
        self.comboBox_window_mode.addItem("")
        self.comboBox_window_mode.addItem("")
        self.comboBox_window_mode.setObjectName(u"comboBox_window_mode")
        sizePolicy1.setHeightForWidth(self.comboBox_window_mode.sizePolicy().hasHeightForWidth())
        self.comboBox_window_mode.setSizePolicy(sizePolicy1)
        self.comboBox_window_mode.setMinimumSize(QSize(300, 0))
        self.comboBox_window_mode.setFont(font2)

        self.horizontalLayout_3.addWidget(self.comboBox_window_mode)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_6.addWidget(self.widget)

        self.card_other_settings = QWidget(SettingsWindow)
        self.card_other_settings.setObjectName(u"card_other_settings")
        sizePolicy2.setHeightForWidth(self.card_other_settings.sizePolicy().hasHeightForWidth())
        self.card_other_settings.setSizePolicy(sizePolicy2)
        self.card_other_settings.setMinimumSize(QSize(0, 100))
        self.card_other_settings.setStyleSheet(u"QWidget {\n"
"    border: 2px solid rgb(50, 50, 50);\n"
"    border-radius: 10px;\n"
"    background-color: rgb(30, 30, 30);\n"
"    padding: 10px;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.card_other_settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_7 = QLabel(self.card_other_settings)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)
        self.label_7.setMinimumSize(QSize(0, 50))
        self.label_7.setFont(font)

        self.verticalLayout.addWidget(self.label_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout.setContentsMargins(-1, 8, -1, 8)
        self.pushButton_other_settings_dec = QPushButton(self.card_other_settings)
        self.pushButton_other_settings_dec.setObjectName(u"pushButton_other_settings_dec")
        sizePolicy1.setHeightForWidth(self.pushButton_other_settings_dec.sizePolicy().hasHeightForWidth())
        self.pushButton_other_settings_dec.setSizePolicy(sizePolicy1)
        self.pushButton_other_settings_dec.setMinimumSize(QSize(50, 50))
        self.pushButton_other_settings_dec.setMaximumSize(QSize(50, 50))
        self.pushButton_other_settings_dec.setSizeIncrement(QSize(50, 50))
        self.pushButton_other_settings_dec.setStyleSheet(u"QPushButton {\n"
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
"QPushButton:hover {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(190, 190, 190);\n"
"    background-color: rgb(100, 100, 100);\n"
"}\n"
"QPushButton:pressed {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}")
        self.pushButton_other_settings_dec.setIcon(icon1)
        self.pushButton_other_settings_dec.setIconSize(QSize(30, 40))

        self.horizontalLayout.addWidget(self.pushButton_other_settings_dec)

        self.lcdNumber_other_settings = QLCDNumber(self.card_other_settings)
        self.lcdNumber_other_settings.setObjectName(u"lcdNumber_other_settings")
        sizePolicy1.setHeightForWidth(self.lcdNumber_other_settings.sizePolicy().hasHeightForWidth())
        self.lcdNumber_other_settings.setSizePolicy(sizePolicy1)
        self.lcdNumber_other_settings.setMinimumSize(QSize(300, 50))

        self.horizontalLayout.addWidget(self.lcdNumber_other_settings)

        self.pushButton_other_settings_add = QPushButton(self.card_other_settings)
        self.pushButton_other_settings_add.setObjectName(u"pushButton_other_settings_add")
        sizePolicy1.setHeightForWidth(self.pushButton_other_settings_add.sizePolicy().hasHeightForWidth())
        self.pushButton_other_settings_add.setSizePolicy(sizePolicy1)
        self.pushButton_other_settings_add.setMinimumSize(QSize(50, 50))
        self.pushButton_other_settings_add.setMaximumSize(QSize(50, 50))
        self.pushButton_other_settings_add.setStyleSheet(u"QPushButton {\n"
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
"QPushButton:hover {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(190, 190, 190);\n"
"    background-color: rgb(100, 100, 100);\n"
"}\n"
"QPushButton:pressed {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}")
        self.pushButton_other_settings_add.setIcon(icon2)
        self.pushButton_other_settings_add.setIconSize(QSize(30, 40))

        self.horizontalLayout.addWidget(self.pushButton_other_settings_add)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_6.addWidget(self.card_other_settings)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 8, -1, 16)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.settings_save = QPushButton(SettingsWindow)
        self.settings_save.setObjectName(u"settings_save")
        self.settings_save.setEnabled(False)
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.settings_save.sizePolicy().hasHeightForWidth())
        self.settings_save.setSizePolicy(sizePolicy5)
        self.settings_save.setMinimumSize(QSize(200, 50))
        self.settings_save.setFont(font)
        self.settings_save.setStyleSheet(u"QPushButton {\n"
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
"QPushButton:hover {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(190, 190, 190);\n"
"    background-color: rgb(100, 100, 100);\n"
"}\n"
"QPushButton:pressed {\n"
"    color: rgb(220,221,229);\n"
"    background-color: rgb(37, 150, 190);\n"
"}")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.settings_save.setIcon(icon3)
        self.settings_save.setIconSize(QSize(32, 32))

        self.horizontalLayout_5.addWidget(self.settings_save)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)


        self.retranslateUi(SettingsWindow)

        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"Settings", None))
        self.settings_back.setText("")
        self.label_6.setText(QCoreApplication.translate("SettingsWindow", u"Settings", None))
        self.label_5.setText(QCoreApplication.translate("SettingsWindow", u"Font Size", None))
        self.label_8.setText(QCoreApplication.translate("SettingsWindow", u"Application Size", None))
        self.comboBox_size.setItemText(0, QCoreApplication.translate("SettingsWindow", u"1600x900 (HD+)", None))
        self.comboBox_size.setItemText(1, QCoreApplication.translate("SettingsWindow", u"1680x1050 (WSXGA+)", None))
        self.comboBox_size.setItemText(2, QCoreApplication.translate("SettingsWindow", u"1920x1080 (Full HD)", None))
        self.comboBox_size.setItemText(3, QCoreApplication.translate("SettingsWindow", u"1920x1200 (WUXGA)", None))
        self.comboBox_size.setItemText(4, QCoreApplication.translate("SettingsWindow", u"2560x1440 (QHD)", None))
        self.comboBox_size.setItemText(5, QCoreApplication.translate("SettingsWindow", u"2560x1600 (WQXGA)", None))
        self.comboBox_size.setItemText(6, QCoreApplication.translate("SettingsWindow", u"3840x2160 (4K UHD)", None))
        self.comboBox_size.setItemText(7, QCoreApplication.translate("SettingsWindow", u"4096x2160 (4K DCI)", None))

        self.comboBox_window_mode.setItemText(0, QCoreApplication.translate("SettingsWindow", u"Window", None))
        self.comboBox_window_mode.setItemText(1, QCoreApplication.translate("SettingsWindow", u"Full Screen", None))

        self.label_7.setText(QCoreApplication.translate("SettingsWindow", u"Other Settings", None))
        self.pushButton_other_settings_dec.setText("")
        self.pushButton_other_settings_add.setText("")
        self.settings_save.setText(QCoreApplication.translate("SettingsWindow", u"Save", None))
    # retranslateUi

