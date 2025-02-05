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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLCDNumber, QLabel,
    QLayout, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_LightCueCalibrationPage(object):
    def setupUi(self, LightCueCalibrationPage):
        if not LightCueCalibrationPage.objectName():
            LightCueCalibrationPage.setObjectName(u"LightCueCalibrationPage")
        LightCueCalibrationPage.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LightCueCalibrationPage.sizePolicy().hasHeightForWidth())
        LightCueCalibrationPage.setSizePolicy(sizePolicy)
        LightCueCalibrationPage.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout = QVBoxLayout(LightCueCalibrationPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header = QHBoxLayout()
        self.header.setObjectName(u"header")
        self.header.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.title = QLabel(LightCueCalibrationPage)
        self.title.setObjectName(u"title")
        self.title.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(36)
        self.title.setFont(font)

        self.header.addWidget(self.title)

        self.horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header.addItem(self.horizontal_spacer)

        self.info_button = QPushButton(LightCueCalibrationPage)
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

        self.status_label = QLabel(LightCueCalibrationPage)
        self.status_label.setObjectName(u"status_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
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

        self.intensity_layout = QHBoxLayout()
        self.intensity_layout.setObjectName(u"intensity_layout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.intensity_layout.addItem(self.horizontalSpacer)

        self.decrease_intensity_button = QPushButton(LightCueCalibrationPage)
        self.decrease_intensity_button.setObjectName(u"decrease_intensity_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.decrease_intensity_button.sizePolicy().hasHeightForWidth())
        self.decrease_intensity_button.setSizePolicy(sizePolicy2)
        self.decrease_intensity_button.setMinimumSize(QSize(50, 0))
        self.decrease_intensity_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.decrease_intensity_button.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #1976D2);\n"
"color: white;\n"
"font-weight: bold;\n"
"padding: 10px;\n"
"border-radius: 5px;")

        self.intensity_layout.addWidget(self.decrease_intensity_button)

        self.intensity_display = QLCDNumber(LightCueCalibrationPage)
        self.intensity_display.setObjectName(u"intensity_display")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.intensity_display.sizePolicy().hasHeightForWidth())
        self.intensity_display.setSizePolicy(sizePolicy3)
        self.intensity_display.setMinimumSize(QSize(100, 0))

        self.intensity_layout.addWidget(self.intensity_display)

        self.increase_intensity_button = QPushButton(LightCueCalibrationPage)
        self.increase_intensity_button.setObjectName(u"increase_intensity_button")
        sizePolicy2.setHeightForWidth(self.increase_intensity_button.sizePolicy().hasHeightForWidth())
        self.increase_intensity_button.setSizePolicy(sizePolicy2)
        self.increase_intensity_button.setMinimumSize(QSize(50, 0))
        self.increase_intensity_button.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #1976D2);\n"
"color: white;\n"
"font-weight: bold;\n"
"padding: 10px;\n"
"border-radius: 5px;")

        self.intensity_layout.addWidget(self.increase_intensity_button)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.intensity_layout.addItem(self.horizontalSpacer_2)


        self.body.addLayout(self.intensity_layout)

        self.cue_button = QPushButton(LightCueCalibrationPage)
        self.cue_button.setObjectName(u"cue_button")
        sizePolicy1.setHeightForWidth(self.cue_button.sizePolicy().hasHeightForWidth())
        self.cue_button.setSizePolicy(sizePolicy1)
        self.cue_button.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196F3, stop:1 #1976D2);\n"
"color: white;\n"
"font-weight: bold;\n"
"padding: 10px;\n"
"border-radius: 5px;")

        self.body.addWidget(self.cue_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.body.addItem(self.verticalSpacer_2)

        self.perception_widget = QWidget(LightCueCalibrationPage)
        self.perception_widget.setObjectName(u"perception_widget")
        self.perception_widget.setEnabled(True)
        self.perception_layout = QHBoxLayout(self.perception_widget)
        self.perception_layout.setObjectName(u"perception_layout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.perception_layout.addItem(self.horizontalSpacer_4)

        self.perception_label = QLabel(self.perception_widget)
        self.perception_label.setObjectName(u"perception_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.perception_label.sizePolicy().hasHeightForWidth())
        self.perception_label.setSizePolicy(sizePolicy4)
        self.perception_label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.1);\n"
"            color: white;\n"
"            padding: 10px;\n"
"            border-radius: 10px;")

        self.perception_layout.addWidget(self.perception_label)

        self.no_button = QPushButton(self.perception_widget)
        self.no_button.setObjectName(u"no_button")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.no_button.sizePolicy().hasHeightForWidth())
        self.no_button.setSizePolicy(sizePolicy5)
        self.no_button.setMinimumSize(QSize(50, 0))
        self.no_button.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #F44336, stop:1 #D32F2F);\n"
"color: white;\n"
"font-weight: bold;\n"
"padding: 10px;\n"
"border-radius: 5px;")

        self.perception_layout.addWidget(self.no_button)

        self.yes_button = QPushButton(self.perception_widget)
        self.yes_button.setObjectName(u"yes_button")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.yes_button.sizePolicy().hasHeightForWidth())
        self.yes_button.setSizePolicy(sizePolicy6)
        self.yes_button.setMinimumSize(QSize(50, 0))
        self.yes_button.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4CAF50, stop:1 #2E7D32);\n"
"                color: white;\n"
"                font-weight: bold;\n"
"                padding: 10px;\n"
"                border-radius: 5px;")

        self.perception_layout.addWidget(self.yes_button)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.perception_layout.addItem(self.horizontalSpacer_3)


        self.body.addWidget(self.perception_widget)


        self.verticalLayout.addLayout(self.body)


        self.retranslateUi(LightCueCalibrationPage)

        QMetaObject.connectSlotsByName(LightCueCalibrationPage)
    # setupUi

    def retranslateUi(self, LightCueCalibrationPage):
        LightCueCalibrationPage.setWindowTitle(QCoreApplication.translate("LightCueCalibrationPage", u"{{ header}}", None))
        self.title.setText(QCoreApplication.translate("LightCueCalibrationPage", u"{{ header }}", None))
        self.info_button.setText("")
        self.status_label.setText("")
        self.decrease_intensity_button.setText(QCoreApplication.translate("LightCueCalibrationPage", u"-", None))
        self.increase_intensity_button.setText(QCoreApplication.translate("LightCueCalibrationPage", u"+", None))
        self.cue_button.setText(QCoreApplication.translate("LightCueCalibrationPage", u"Present Cue", None))
        self.perception_label.setText(QCoreApplication.translate("LightCueCalibrationPage", u"Did you perceive the cue", None))
        self.no_button.setText(QCoreApplication.translate("LightCueCalibrationPage", u"No", None))
        self.yes_button.setText(QCoreApplication.translate("LightCueCalibrationPage", u"Yes", None))
    # retranslateUi

