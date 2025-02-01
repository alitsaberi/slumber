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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QLayout,
    QListView, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)

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
        self.stacked_widget = QStackedWidget(ProcedurePage)
        self.stacked_widget.setObjectName(u"stacked_widget")
        sizePolicy.setHeightForWidth(self.stacked_widget.sizePolicy().hasHeightForWidth())
        self.stacked_widget.setSizePolicy(sizePolicy)
        self.stacked_widget.setMaximumSize(QSize(3840, 2160))

        self.horizontalLayout.addWidget(self.stacked_widget)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setObjectName(u"vertical_layout")
        self.vertical_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.vertical_layout.setContentsMargins(-1, -1, 8, 8)
        self.task_list = QListWidget(ProcedurePage)
        self.task_list.setObjectName(u"task_list")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.task_list.sizePolicy().hasHeightForWidth())
        self.task_list.setSizePolicy(sizePolicy1)
        self.task_list.setMinimumSize(QSize(400, 0))
        self.task_list.setMaximumSize(QSize(3840, 2160))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        self.task_list.setFont(font)
        self.task_list.setStyleSheet(u"/* Style for the QListWidget */\n"
"                                            QListWidget {\n"
"                                            background-color: #F5F5F5;\n"
"                                            border: 1px solid #CCCCCC;\n"
"                                            border-radius: 8px;\n"
"                                            padding: 5px;\n"
"                                            }\n"
"\n"
"                                            /* Style for QListWidgetItem (Default/Inactive) */\n"
"                                            QListWidget::item {\n"
"                                            background-color: #FFFFFF;\n"
"                                            border: 1px solid #E0E0E0;\n"
"                                            border-radius: 5px;\n"
"                                            margin: 16px;\n"
"                                            padding: 6px;\n"
"                                            color: #555555; /* Text color for inact"
                        "ive items */\n"
"                                            }\n"
"\n"
"                                            /* Style for selected QListWidgetItem */\n"
"                                            QListWidget::item:selected {\n"
"                                            background-color: #D0E7FF;\n"
"                                            border: 2px solid #3399FF;\n"
"                                            color: #000000; /* Text color for selected items */\n"
"                                            }\n"
"\n"
"                                            /* Style for hovered QListWidgetItem */\n"
"                                            QListWidget::item:hover {\n"
"                                            background-color: #E6F2FF;\n"
"                                            border: 1px solid #66B2FF;\n"
"                                            color: #333333; /* Text color on hover */\n"
"                                            }\n"
"\n"
"                         "
                        "                   /* Style for disabled QListWidgetItem */\n"
"                                            QListWidget::item:disabled {\n"
"                                            background-color: #F0F0F0;\n"
"                                            border: 1px solid #D3D3D3;\n"
"                                            color: #A9A9A9; /* Grey text for disabled items */\n"
"                                            }\n"
"\n"
"                                            /* Style for QLabel within the items */\n"
"                                            QLabel {\n"
"                                            color: #555555;\n"
"                                            font-size: 14px;\n"
"                                            }\n"
"\n"
"                                            /* Optional: Alternating item backgrounds for better\n"
"                                            readability */\n"
"                                            QListWidget::item:nth-child(even) {\n"
"   "
                        "                                         background-color: #FAFAFA;\n"
"                                            }\n"
"\n"
"                                            QListWidget::item:nth-child(odd) {\n"
"                                            background-color: #FFFFFF;\n"
"                                            }")
        self.task_list.setAutoScroll(False)
        self.task_list.setAutoScrollMargin(8)
        self.task_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.task_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.task_list.setMovement(QListView.Movement.Static)
        self.task_list.setProperty(u"isWrapping", True)
        self.task_list.setResizeMode(QListView.ResizeMode.Adjust)
        self.task_list.setGridSize(QSize(385, 60))
        self.task_list.setUniformItemSizes(False)
        self.task_list.setWordWrap(True)
        self.task_list.setSelectionRectVisible(True)

        self.vertical_layout.addWidget(self.task_list)

        self.done_button = QPushButton(ProcedurePage)
        self.done_button.setObjectName(u"done_button")
        self.done_button.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.done_button.sizePolicy().hasHeightForWidth())
        self.done_button.setSizePolicy(sizePolicy2)
        self.done_button.setMinimumSize(QSize(0, 35))
        self.done_button.setStyleSheet(u"QPushButton {\n"
"                                                    color: rgb(255, 255, 255);\n"
"                                                    background-color: rgb(1, 92, 187);\n"
"                                                    border: 1px;\n"
"                                                    border-radius: 10px;\n"
"                                                    }\n"
"\n"
"                                                    QPushButton:hover {\n"
"                                                    color: rgb(220,221,229);\n"
"                                                    background-color: rgb(37, 150, 190);\n"
"                                                    }\n"
"\n"
"                                                    QPushButton:pressed {\n"
"                                                    color: rgb(220,221,229);\n"
"                                                    background-color: rgb(37, 150, 190);\n"
"                                                    }\n"
"\n"
""
                        "                                                    QPushButton:disabled {\n"
"                                                    color: rgb(190, 190, 190);\n"
"                                                    background-color: rgb(100, 100, 100);\n"
"                                                    }")

        self.vertical_layout.addWidget(self.done_button)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName(u"horizontal_layout")
        self.horizontal_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontal_layout.setContentsMargins(-1, 0, -1, -1)
        self.previous_button = QPushButton(ProcedurePage)
        self.previous_button.setObjectName(u"previous_button")
        sizePolicy2.setHeightForWidth(self.previous_button.sizePolicy().hasHeightForWidth())
        self.previous_button.setSizePolicy(sizePolicy2)
        self.previous_button.setMinimumSize(QSize(100, 35))
        self.previous_button.setMaximumSize(QSize(200, 50))
        self.previous_button.setStyleSheet(u"QPushButton {\n"
"                                                    color: rgb(255, 255, 255);\n"
"                                                    background-color: rgb(1, 92, 187);\n"
"                                                    border: 1px;\n"
"                                                    border-radius: 10px;\n"
"                                                    }\n"
"\n"
"                                                    QPushButton:hover {\n"
"                                                    color: rgb(220,221,229);\n"
"                                                    background-color: rgb(37, 150, 190);\n"
"                                                    }\n"
"\n"
"                                                    QPushButton:pressed {\n"
"                                                    color: rgb(220,221,229);\n"
"                                                    background-color: rgb(37, 150, 190);\n"
"                                                    }\n"
"\n"
""
                        "                                                    QPushButton:disabled {\n"
"                                                    color: rgb(190, 190, 190);\n"
"                                                    background-color: rgb(100, 100, 100);\n"
"                                                    }")

        self.horizontal_layout.addWidget(self.previous_button)

        self.next_button = QPushButton(ProcedurePage)
        self.next_button.setObjectName(u"next_button")
        sizePolicy2.setHeightForWidth(self.next_button.sizePolicy().hasHeightForWidth())
        self.next_button.setSizePolicy(sizePolicy2)
        self.next_button.setMinimumSize(QSize(100, 35))
        self.next_button.setMaximumSize(QSize(200, 50))
        self.next_button.setStyleSheet(u"QPushButton {\n"
"                                                    color: rgb(255, 255, 255);\n"
"                                                    background-color: rgb(1, 92, 187);\n"
"                                                    border: 1px;\n"
"                                                    border-radius: 10px;\n"
"                                                    }\n"
"\n"
"                                                    QPushButton:hover {\n"
"                                                    color: rgb(220,221,229);\n"
"                                                    background-color: rgb(37, 150, 190);\n"
"                                                    }\n"
"\n"
"                                                    QPushButton:pressed {\n"
"                                                    color: rgb(220,221,229);\n"
"                                                    background-color: rgb(37, 150, 190);\n"
"                                                    }\n"
"\n"
""
                        "                                                    QPushButton:disabled {\n"
"                                                    color: rgb(190, 190, 190);\n"
"                                                    background-color: rgb(100, 100, 100);\n"
"                                                    }")

        self.horizontal_layout.addWidget(self.next_button)


        self.vertical_layout.addLayout(self.horizontal_layout)


        self.horizontalLayout.addLayout(self.vertical_layout)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(ProcedurePage)

        self.task_list.setCurrentRow(-1)


        QMetaObject.connectSlotsByName(ProcedurePage)
    # setupUi

    def retranslateUi(self, ProcedurePage):
        ProcedurePage.setWindowTitle(QCoreApplication.translate("ProcedurePage", u"Widget", None))
        self.done_button.setText(QCoreApplication.translate("ProcedurePage", u"Done", None))
        self.previous_button.setText(QCoreApplication.translate("ProcedurePage", u"Previous", None))
        self.next_button.setText(QCoreApplication.translate("ProcedurePage", u"Next", None))
    # retranslateUi

