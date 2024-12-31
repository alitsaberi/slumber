from PySide6.QtWidgets import QWidget, QStackedWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Signal
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

        # Connect buttons
        self.nextButton.clicked.connect(self.next_page)
        self.prevButton.clicked.connect(self.prev_page)

    def load_config(self, tasks):
        for task in tasks:
            module_path = task['module']
            print("-----------------")
            print(module_path)
            module = importlib.import_module(module_path + '.widget')
            widget_class = getattr(module, 'WidgetPage')
            widget_instance = widget_class()
            self.procedureStack.addWidget(widget_instance)

        if self.procedureStack.count() > 0:
            self.procedureStack.setCurrentIndex(0)

    def next_page(self):
        if self.current_index < self.procedureStack.count() - 1:
            self.current_index += 1
            self.procedureStack.setCurrentIndex(self.current_index)
            self.page_changed_signal.emit()

    def prev_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.procedureStack.setCurrentIndex(self.current_index)
            self.page_changed_signal.emit()