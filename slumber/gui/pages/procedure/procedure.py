from PySide6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QRadioButton,
    QLabel,
    QButtonGroup,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem
from .procedure_ui import Ui_ProcedurePage
import importlib


class ProcedurePage(QWidget, Ui_ProcedurePage):
    page_changed_signal = Signal()

    def __init__(self, tasks, parent=None):
        super(ProcedurePage, self).__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.tasks = sorted(tasks, key=lambda x: x['task_id'])
        self.current_index = 0
        self.load_config(self.tasks)

        # Connect navigation buttons
        self.nextButton.clicked.connect(self.next_page)
        self.prevButton.clicked.connect(self.prev_page)

        # Connect list selection change
        self.procedureStepList.currentRowChanged.connect(self.on_list_selection_changed)

    def load_config(self, tasks):
        """
        Load the configuration of tasks into the procedureStepList and stacked widget.
        """
        # Initialize QListWidget
        self.procedureStepList.clear()

        # Populate the QListWidget with custom widgets containing radio buttons and labels
        for idx, task in enumerate(tasks):
            item = QListWidgetItem()
            item.setText(f"{idx + 1}. {task['name']}")

            self.procedureStepList.addItem(item)


        # Load widgets into the stacked widget
        for task in tasks:
            module_path = task['module']
            print("-----------------")
            print(module_path)
            try:
                module = importlib.import_module(f"{module_path}.widget")
                widget_class = getattr(module, 'WidgetPage')
                widget_instance = widget_class()
                self.procedureStack.addWidget(widget_instance)
            except (ImportError, AttributeError) as e:
                print(f"Error loading module {module_path}: {e}")

        if self.procedureStack.count() > 0:
            print("Setting current index to 0")
            self.procedureStepList.setCurrentRow(0)


    def next_page(self):
        if self.current_index < self.procedureStack.count() - 1:
            self.current_index += 1
            self.procedureStack.setCurrentIndex(self.current_index)
            self.procedureStepList.setCurrentRow(self.current_index)
            self.page_changed_signal.emit()

    def prev_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.procedureStack.setCurrentIndex(self.current_index)
            self.procedureStepList.setCurrentRow(self.current_index)
            self.page_changed_signal.emit()

    def on_list_selection_changed(self, currentRow):
        self.current_index = currentRow
        self.procedureStack.setCurrentIndex(self.current_index)
        self.page_changed_signal.emit()