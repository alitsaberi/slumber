
################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_Widget:
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName("Widget")
        Widget.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.widget_title = QLabel(Widget)
        self.widget_title.setObjectName("widget_title")
        self.widget_title.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(36)
        self.widget_title.setFont(font)

        self.horizontalLayout_4.addWidget(self.widget_title)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.button_info = QPushButton(Widget)
        self.button_info.setObjectName("button_info")
        self.button_info.setMinimumSize(QSize(50, 50))
        self.button_info.setMaximumSize(QSize(50, 50))
        self.button_info.setStyleSheet("QPushButton {\n"
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

        self.widget_body = QWidget(Widget)
        self.widget_body.setObjectName("widget_body")
        sizePolicy.setHeightForWidth(self.widget_body.sizePolicy().hasHeightForWidth())
        self.widget_body.setSizePolicy(sizePolicy)
        self.widget_body.setMaximumSize(QSize(3840, 2160))
        self.label_body = QLabel(self.widget_body)
        self.label_body.setObjectName("label_body")
        self.label_body.setGeometry(QRect(200, 160, 391, 211))
        font1 = QFont()
        font1.setBold(False)
        self.label_body.setFont(font1)

        self.verticalLayout.addWidget(self.widget_body)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", "Put on and start headband", None))
        self.widget_title.setText(QCoreApplication.translate("Widget", "Put on and start headband", None))
        self.button_info.setText("")
        self.label_body.setText(QCoreApplication.translate("Widget", "Put on and start headband works correctly.", None))
    # retranslateUi

