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
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        HelpDialog.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HelpDialog.sizePolicy().hasHeightForWidth())
        HelpDialog.setSizePolicy(sizePolicy)
        HelpDialog.setMinimumSize(QSize(400, 300))
        self.verticalLayout = QVBoxLayout(HelpDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.body = QWidget(HelpDialog)
        self.body.setObjectName(u"body")
        sizePolicy.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy)
        self.body.setMaximumSize(QSize(3840, 2160))

        self.verticalLayout.addWidget(self.body)


        self.retranslateUi(HelpDialog)

        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", u"Information", None))
    # retranslateUi

