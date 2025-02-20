# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QPushButton,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_HomePage(object):
    def setupUi(self, HomePage):
        if not HomePage.objectName():
            HomePage.setObjectName(u"HomePage")
        HomePage.setWindowModality(Qt.WindowModality.NonModal)
        HomePage.resize(1596, 1280)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HomePage.sizePolicy().hasHeightForWidth())
        HomePage.setSizePolicy(sizePolicy)
        HomePage.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout_5 = QVBoxLayout(HomePage)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.web_engine_view = QWebEngineView(HomePage)
        self.web_engine_view.setObjectName(u"web_engine_view")
        sizePolicy.setHeightForWidth(self.web_engine_view.sizePolicy().hasHeightForWidth())
        self.web_engine_view.setSizePolicy(sizePolicy)
        self.web_engine_view.setMinimumSize(QSize(0, 0))

        self.verticalLayout_5.addWidget(self.web_engine_view)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName(u"horizontal_layout")
        self.horizontal_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.start_button = QPushButton(HomePage)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setMinimumSize(QSize(400, 60))
        self.start_button.setMaximumSize(QSize(400, 60))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(18)
        self.start_button.setFont(font)
        self.start_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.start_button.setStyleSheet(u"QPushButton {\n"
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

        self.horizontal_layout.addWidget(self.start_button)


        self.verticalLayout_5.addLayout(self.horizontal_layout)

        self.overview_label = QLabel(HomePage)
        self.overview_label.setObjectName(u"overview_label")
        self.overview_label.setMaximumSize(QSize(16777215, 50))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(24)
        self.overview_label.setFont(font1)

        self.verticalLayout_5.addWidget(self.overview_label)

        self.overview_table = QTableView(HomePage)
        self.overview_table.setObjectName(u"overview_table")
        self.overview_table.setMaximumSize(QSize(16777215, 300))
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(14)
        self.overview_table.setFont(font2)
        self.overview_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.overview_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout_5.addWidget(self.overview_table)


        self.retranslateUi(HomePage)

        QMetaObject.connectSlotsByName(HomePage)
    # setupUi

    def retranslateUi(self, HomePage):
        HomePage.setWindowTitle(QCoreApplication.translate("HomePage", u"Home", None))
        self.start_button.setText(QCoreApplication.translate("HomePage", u"Start", None))
        self.overview_label.setText(QCoreApplication.translate("HomePage", u"Overview", None))
    # retranslateUi

