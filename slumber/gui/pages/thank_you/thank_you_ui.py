
################################################################################
## Form generated from reading UI file 'thank_you.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)


class Ui_ThankYouPage:
    def setupUi(self, ThankYouPage):
        if not ThankYouPage.objectName():
            ThankYouPage.setObjectName("ThankYouPage")
        ThankYouPage.setWindowModality(Qt.WindowModality.NonModal)
        ThankYouPage.resize(666, 566)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ThankYouPage.sizePolicy().hasHeightForWidth())
        ThankYouPage.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(ThankYouPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 16)
        self.thank_you_back = QPushButton(ThankYouPage)
        self.thank_you_back.setObjectName("thank_you_back")
        self.thank_you_back.setMinimumSize(QSize(50, 50))
        self.thank_you_back.setMaximumSize(QSize(50, 50))
        self.thank_you_back.setSizeIncrement(QSize(50, 50))
        self.thank_you_back.setStyleSheet("QPushButton {\n"
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
        self.thank_you_back.setIcon(icon)
        self.thank_you_back.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.thank_you_back)

        self.horizontalSpacer_7 = QSpacerItem(40, 50, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.webEngineView_thank_you = QWebEngineView(ThankYouPage)
        self.webEngineView_thank_you.setObjectName("webEngineView_thank_you")
        sizePolicy.setHeightForWidth(self.webEngineView_thank_you.sizePolicy().hasHeightForWidth())
        self.webEngineView_thank_you.setSizePolicy(sizePolicy)
        self.webEngineView_thank_you.setMinimumSize(QSize(0, 0))
        self.webEngineView_thank_you.setMaximumSize(QSize(3840, 2160))

        self.verticalLayout_3.addWidget(self.webEngineView_thank_you)


        self.retranslateUi(ThankYouPage)

        QMetaObject.connectSlotsByName(ThankYouPage)
    # setupUi

    def retranslateUi(self, ThankYouPage):
        ThankYouPage.setWindowTitle(QCoreApplication.translate("ThankYouPage", "Help", None))
        self.thank_you_back.setText("")
    # retranslateUi

