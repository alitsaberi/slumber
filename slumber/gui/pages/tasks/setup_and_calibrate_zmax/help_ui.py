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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HelpDialog.sizePolicy().hasHeightForWidth())
        HelpDialog.setSizePolicy(sizePolicy)
        HelpDialog.setMinimumSize(QSize(400, 300))
        self.verticalLayout = QVBoxLayout(HelpDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_body = QWidget(HelpDialog)
        self.widget_body.setObjectName(u"widget_body")
        sizePolicy.setHeightForWidth(self.widget_body.sizePolicy().hasHeightForWidth())
        self.widget_body.setSizePolicy(sizePolicy)
        self.widget_body.setMaximumSize(QSize(3840, 2160))
        self.label_body = QLabel(self.widget_body)
        self.label_body.setObjectName(u"label_body")
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.label_body.setFont(font)

        self.verticalLayout.addWidget(self.widget_body)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer)

        self.button_ok = QPushButton(HelpDialog)
        self.button_ok.setObjectName(u"button_ok")

        self.buttonLayout.addWidget(self.button_ok)

        self.button_cancel = QPushButton(HelpDialog)
        self.button_cancel.setObjectName(u"button_cancel")

        self.buttonLayout.addWidget(self.button_cancel)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(HelpDialog)

        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", u"Slumber - Setup and calibrate ZMax", None))
        self.label_body.setText(QCoreApplication.translate("HelpDialog", u"Setup and calibrate ZMax - dialog window works.", None))
        self.button_ok.setText(QCoreApplication.translate("HelpDialog", u"OK", None))
        self.button_cancel.setText(QCoreApplication.translate("HelpDialog", u"Cancel", None))
    # retranslateUi

