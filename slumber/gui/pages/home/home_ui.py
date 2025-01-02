
################################################################################
## Form generated from reading UI file 'home.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractScrollArea,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
)


class Ui_HomePage:
    def setupUi(self, HomePage):
        if not HomePage.objectName():
            HomePage.setObjectName("HomePage")
        HomePage.setWindowModality(Qt.WindowModality.NonModal)
        HomePage.resize(1596, 1280)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HomePage.sizePolicy().hasHeightForWidth())
        HomePage.setSizePolicy(sizePolicy)
        HomePage.setMaximumSize(QSize(3840, 2160))
        self.verticalLayout_5 = QVBoxLayout(HomePage)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.webEngineView_main = QWebEngineView(HomePage)
        self.webEngineView_main.setObjectName("webEngineView_main")
        sizePolicy.setHeightForWidth(self.webEngineView_main.sizePolicy().hasHeightForWidth())
        self.webEngineView_main.setSizePolicy(sizePolicy)
        self.webEngineView_main.setMinimumSize(QSize(0, 0))

        self.verticalLayout_5.addWidget(self.webEngineView_main)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.pushButton_start_procedure = QPushButton(HomePage)
        self.pushButton_start_procedure.setObjectName("pushButton_start_procedure")
        self.pushButton_start_procedure.setMinimumSize(QSize(400, 60))
        self.pushButton_start_procedure.setMaximumSize(QSize(400, 60))
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(18)
        self.pushButton_start_procedure.setFont(font)
        self.pushButton_start_procedure.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_start_procedure.setStyleSheet("QPushButton {\n"
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

        self.horizontalLayout_6.addWidget(self.pushButton_start_procedure)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.label_diary = QLabel(HomePage)
        self.label_diary.setObjectName("label_diary")
        self.label_diary.setMaximumSize(QSize(16777215, 50))
        font1 = QFont()
        font1.setFamilies(["Arial"])
        font1.setPointSize(24)
        self.label_diary.setFont(font1)

        self.verticalLayout_5.addWidget(self.label_diary)

        self.tableView_diary = QTableView(HomePage)
        self.tableView_diary.setObjectName("tableView_diary")
        self.tableView_diary.setMaximumSize(QSize(16777215, 300))
        font2 = QFont()
        font2.setFamilies(["Arial"])
        font2.setPointSize(14)
        self.tableView_diary.setFont(font2)
        self.tableView_diary.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableView_diary.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout_5.addWidget(self.tableView_diary)


        self.retranslateUi(HomePage)

        QMetaObject.connectSlotsByName(HomePage)
    # setupUi

    def retranslateUi(self, HomePage):
        HomePage.setWindowTitle(QCoreApplication.translate("HomePage", "Home", None))
        self.pushButton_start_procedure.setText(QCoreApplication.translate("HomePage", "Start Procedure", None))
        self.label_diary.setText(QCoreApplication.translate("HomePage", "Diary", None))
    # retranslateUi

