# FILE: home.py

import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QBrush, QColor, QFont, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QWidget

from ....models.study_calendar_model import get_todays_day_number
from ....models.task_progress_model import get_diary
from .home_ui import Ui_HomePage


class HomePage(QWidget, Ui_HomePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.pushButton_start_procedure.clicked.connect(self.on_start_procedure_clicked)

        # Load the HTML file
        base_dir = os.path.dirname(__file__)
        html_file_path = os.path.join(base_dir, "./assets/html/index.html")
        self.webEngineView_main.setUrl(QUrl.fromLocalFile(html_file_path))

        # Populate the diary table
        self.populate_diary_table()

    def on_start_procedure_clicked(self):
        print("Start Procedure button pressed")

    def populate_diary_table(self):
        diary = get_diary()
        today_day = get_todays_day_number()

        all_days = sorted(set(x["task_day"] for x in diary))
        all_types = sorted(set(x["type"] for x in diary))

        model = QStandardItemModel(len(all_types), len(all_days))
        for col, day in enumerate(all_days):
            text = f"Day {day}"
            model.setHeaderData(col, Qt.Horizontal, text, Qt.DisplayRole)
            if day == today_day:
                font = model.headerData(col, Qt.Horizontal, Qt.FontRole) or QFont()
                font.setBold(True)
                model.setHeaderData(col, Qt.Horizontal, font, Qt.FontRole)
                model.setHeaderData(
                    col, Qt.Horizontal, QBrush(QColor("green")), Qt.ForegroundRole
                )
            elif day > today_day:
                model.setHeaderData(
                    col, Qt.Horizontal, QBrush(QColor("gray")), Qt.ForegroundRole
                )

        for row, t in enumerate(all_types):
            # Map types to custom labels
            if t == "pre_processing":
                label = "Pre Processing"
            elif t == "post_processing":
                label = "Post Processing"
            elif t == "recording":
                label = "Recording"
            else:
                label = t
            model.setHeaderData(row, Qt.Vertical, label)

            for col, day in enumerate(all_days):
                tasks = [x for x in diary if x["task_day"] == day and x["type"] == t]
                statuses = set(x["status"] for x in tasks)
                if "progress" in statuses:
                    combined = "progress"
                elif "skipped" in statuses:
                    combined = "skipped"
                elif "open" in statuses:
                    combined = "open" if len(statuses) == 1 else "progress"
                else:
                    combined = "done"

                cell = QStandardItem(combined)
                if combined == "open":
                    cell.setBackground(QColor("Gray"))
                elif combined == "progress":
                    cell.setBackground(QColor("Red"))
                elif combined == "skipped":
                    cell.setBackground(QColor("orange"))
                elif combined == "done":
                    cell.setBackground(QColor("Green"))
                model.setItem(row, col, cell)

        self.tableView_diary.setModel(model)
        self.tableView_diary.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_diary.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableView_diary.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.tableView_diary.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
