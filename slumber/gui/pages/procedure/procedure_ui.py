# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'procedure.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_ProcedurePage(object):
    def setupUi(self, ProcedurePage):
        if not ProcedurePage.objectName():
            ProcedurePage.setObjectName(u"ProcedurePage")
        ProcedurePage.resize(1267, 877)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProcedurePage.sizePolicy().hasHeightForWidth())
        ProcedurePage.setSizePolicy(sizePolicy)
        ProcedurePage.setMaximumSize(QSize(3840, 2160))
        self.horizontalLayout_2 = QHBoxLayout(ProcedurePage)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.procedureStack = QStackedWidget(ProcedurePage)
        self.procedureStack.setObjectName(u"procedureStack")
        sizePolicy.setHeightForWidth(self.procedureStack.sizePolicy().hasHeightForWidth())
        self.procedureStack.setSizePolicy(sizePolicy)
        self.procedureStack.setMaximumSize(QSize(3840, 2160))

        self.horizontalLayout.addWidget(self.procedureStack)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout.setContentsMargins(-1, -1, 8, 8)
        self.procedureStepList = QListWidget(ProcedurePage)
        self.procedureStepList.setObjectName(u"procedureStepList")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.procedureStepList.sizePolicy().hasHeightForWidth())
        self.procedureStepList.setSizePolicy(sizePolicy1)
        self.procedureStepList.setMinimumSize(QSize(400, 0))
        self.procedureStepList.setMaximumSize(QSize(3840, 2160))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        self.procedureStepList.setFont(font)

        self.verticalLayout.addWidget(self.procedureStepList)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.prevButton = QPushButton(ProcedurePage)
        self.prevButton.setObjectName(u"prevButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.prevButton.sizePolicy().hasHeightForWidth())
        self.prevButton.setSizePolicy(sizePolicy2)
        self.prevButton.setMinimumSize(QSize(100, 35))
        self.prevButton.setMaximumSize(QSize(200, 50))
        self.prevButton.setStyleSheet(u"QPushButton {\n"
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
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(190, 190, 190);\n"
"    background-color: rgb(100, 100, 100);\n"
"}")

        self.horizontalLayout_3.addWidget(self.prevButton)

        self.nextButton = QPushButton(ProcedurePage)
        self.nextButton.setObjectName(u"nextButton")
        sizePolicy2.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy2)
        self.nextButton.setMinimumSize(QSize(100, 35))
        self.nextButton.setMaximumSize(QSize(200, 50))
        self.nextButton.setStyleSheet(u"QPushButton {\n"
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
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: rgb(190, 190, 190);\n"
"    background-color: rgb(100, 100, 100);\n"
"}")

        self.horizontalLayout_3.addWidget(self.nextButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(ProcedurePage)

        QMetaObject.connectSlotsByName(ProcedurePage)
    # setupUi

    def retranslateUi(self, ProcedurePage):
        ProcedurePage.setWindowTitle(QCoreApplication.translate("ProcedurePage", u"Widget", None))
        self.prevButton.setText(QCoreApplication.translate("ProcedurePage", u"Previous", None))
        self.nextButton.setText(QCoreApplication.translate("ProcedurePage", u"Next", None))
    # retranslateUi

