
################################################################################
## Form generated from reading UI file 'help.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_HelpDialog:
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName("HelpDialog")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HelpDialog.sizePolicy().hasHeightForWidth())
        HelpDialog.setSizePolicy(sizePolicy)
        HelpDialog.setMinimumSize(QSize(400, 300))
        self.verticalLayout = QVBoxLayout(HelpDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_body = QWidget(HelpDialog)
        self.widget_body.setObjectName("widget_body")
        sizePolicy.setHeightForWidth(self.widget_body.sizePolicy().hasHeightForWidth())
        self.widget_body.setSizePolicy(sizePolicy)
        self.widget_body.setMaximumSize(QSize(3840, 2160))
        self.label_body = QLabel(self.widget_body)
        self.label_body.setObjectName("label_body")
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        self.label_body.setFont(font)

        self.verticalLayout.addWidget(self.widget_body)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.horizontalSpacer)

        self.button_ok = QPushButton(HelpDialog)
        self.button_ok.setObjectName("button_ok")

        self.buttonLayout.addWidget(self.button_ok)

        self.button_cancel = QPushButton(HelpDialog)
        self.button_cancel.setObjectName("button_cancel")

        self.buttonLayout.addWidget(self.button_cancel)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(HelpDialog)

        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", "Slumber - Fill in Pre-Sleeping Survey", None))
        self.label_body.setText(QCoreApplication.translate("HelpDialog", "Pre-Sleeping Survey - dialog window works.", None))
        self.button_ok.setText(QCoreApplication.translate("HelpDialog", "OK", None))
        self.button_cancel.setText(QCoreApplication.translate("HelpDialog", "Cancel", None))
    # retranslateUi

