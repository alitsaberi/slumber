import importlib

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QListWidgetItem,
    QWidget,
)

from .procedure_ui import Ui_ProcedurePage


class ProcedurePage(QWidget, Ui_ProcedurePage):
    page_changed_signal = Signal()
    procedure_completed_signal = Signal()

    def __init__(self, tasks, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.tasks = sorted(tasks, key=lambda x: x["task_id"])
        self.current_index = 0
        self.widgets = []  # Initialize the widget list
        self.completed_tasks = set()  # Track completed task indices
        self.load_config(self.tasks)

        # Connect navigation buttons
        self.nextButton.clicked.connect(self.next_page)
        self.prevButton.clicked.connect(self.prev_page)

        # Connect list selection change
        self.procedureStepList.currentRowChanged.connect(self.on_list_selection_changed)

    def load_config(self, tasks):
        # Initialize QListWidget
        print(tasks)
        self.procedureStepList.clear()
        self.completed_tasks = set()

        # Populate the QListWidget and QStackedWidget with the tasks
        for idx, task in enumerate(tasks):
            # QListWidget
            item = QListWidgetItem()
            item.setText(f"{idx + 1}. {task['name']}")
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            self.procedureStepList.addItem(item)

            # QStackedWidget
            module_path = task["module"]
            print("-----------------")
            print(module_path)
            try:
                module = importlib.import_module(f"{module_path}.widget")
                widget_class = module.WidgetPage
                widget_instance = widget_class(index=idx)  # Pass the index
                self.procedureStack.addWidget(widget_instance)

                # Store the widget instance in the list
                self.widgets.append(widget_instance)

                # Connect the is_done_signal to the handler
                widget_instance.is_done_signal.connect(self.handle_widget_done)

            except (ImportError, AttributeError) as e:
                print(f"Error loading module {module_path}: {e}")

        if self.procedureStack.count() > 0:
            print("Setting current index to 0")
            self.current_index = 0
            self.procedureStepList.setCurrentRow(0)
            # Activate the first task
            self.activate_task(0)
            # Disable all upcoming tasks
            for idx in range(1, self.procedureStack.count()):
                item = self.procedureStepList.item(idx)
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)  # Keep them disabled
            # Disable navigation buttons initially
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(False)
            # Call the start method of the first widget
            self.widgets[0].start()

    def activate_task(self, index):
        if 0 <= index < self.procedureStepList.count():
            item = self.procedureStepList.item(index)
            item.setFlags(item.flags() | Qt.ItemIsEnabled)

    def mark_task_completed(self, index):
        if 0 <= index < self.procedureStepList.count():
            item = self.procedureStepList.item(index)
            item.setBackground(Qt.green)  # Set background color to green
            item.setText(f"{index + 1}. {item.text().split('. ', 1)[1]} ✅")
            self.completed_tasks.add(index)

    def update_navigation_buttons(self):
        # Previous Button
        self.nextButton.setText("Next")
        if self.current_index > 0:
            self.prevButton.setEnabled(True)
        else:
            self.prevButton.setEnabled(False)

        # Next Button
        if self.current_index < self.procedureStack.count() - 1:
            # Only enable Next if the next task is completed or active
            self.nextButton.setEnabled(len(self.completed_tasks) > self.current_index)
        else:
            self.nextButton.setEnabled(False)

        if self.current_index == self.procedureStack.count() - 1:
            self.nextButton.setText("Complete")
            self.nextButton.setEnabled(True)

    def handle_widget_done(self, index):
        print(f"Widget at index {index} signaled completion.")
        # Mark the current task as completed
        self.mark_task_completed(index)

        # Enable the next task if it exists
        next_index = index + 1
        if next_index < self.procedureStack.count():
            self.activate_task(next_index)

        # Update navigation buttons
        self.update_navigation_buttons()

    def next_page(self):
        if self.current_index < self.procedureStack.count() - 1:
            self.current_index += 1
            self.procedureStack.setCurrentIndex(self.current_index)
            self.procedureStepList.setCurrentRow(self.current_index)
            self.page_changed_signal.emit()
            print(f"Navigated to page {self.current_index}")
            # Call the start method of the new current widget
            self.widgets[self.current_index].start()
            # Update navigation buttons
            self.update_navigation_buttons()
        else:
            print("Procedure completed")
            self.procedure_completed_signal.emit()

    def prev_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.procedureStack.setCurrentIndex(self.current_index)
            self.procedureStepList.setCurrentRow(self.current_index)
            self.page_changed_signal.emit()
            print(f"Navigated to page {self.current_index}")
            # Call the start method of the new current widget
            self.widgets[self.current_index].start()
            # Update navigation buttons
            self.update_navigation_buttons()

    def on_list_selection_changed(self, currentRow):
        self.current_index = currentRow
        self.procedureStack.setCurrentIndex(self.current_index)
        self.page_changed_signal.emit()
        print(f"List selection changed to {currentRow}")
        # Call the start method of the selected widget
        self.widgets[self.current_index].start()
        # Update navigation buttons
        self.update_navigation_buttons()
