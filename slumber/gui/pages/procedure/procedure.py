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

    def load_config(self, tasks):
        """
        Load the configuration of tasks into the procedureStepList and stacked widget.
        """
        # Initialize QListWidget
        self.procedureStepList.clear()
        self.procedureStepList.setSelectionMode(QListWidget.NoSelection)
        self.procedureStepList.setFocusPolicy(Qt.NoFocus)

        # Create a button group for radio buttons
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        # Populate the QListWidget with custom widgets containing radio buttons and labels
        for idx, task in enumerate(tasks):
            item = QListWidgetItem(self.procedureStepList)
            item.setSizeHint(QSize(0, 50))  # Adjust the height as needed

            widget, radio_button = self.create_list_item_widget(idx, task['name'], self.button_group)
            self.procedureStepList.setItemWidget(item, widget)


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
            self.procedureStack.setCurrentIndex(0)

    def create_list_item_widget(self, index, task_name, button_group):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)  # Increased margins for better spacing
        layout.setSpacing(20)  # Increased spacing between elements

        radio_button = QRadioButton()
        radio_button.setChecked(index == 0)
        radio_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        button_group.addButton(radio_button, id=index)

        label = QLabel(f"{index + 1}. {task_name}")
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(radio_button)
        layout.addWidget(label)
        layout.addStretch()

        widget.setLayout(layout)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        radio_button.toggled.connect(lambda checked, idx=index: self.on_radio_toggled(checked, idx))

        return widget, radio_button

    def on_radio_toggled(self, checked, index):
        if checked:
            self.current_index = index
            self.procedureStack.setCurrentIndex(self.current_index)
            self.page_changed_signal.emit()

            # Optionally, highlight the selected item in the list
            item = self.procedureStepList.item(index)
            self.procedureStepList.setCurrentItem(item)

    def next_page(self):
        if self.current_index < self.procedureStack.count() - 1:
            self.current_index += 1
            self.procedureStack.setCurrentIndex(self.current_index)
            self.button_group.button(self.current_index).setChecked(True)  # Update radio button
            self.page_changed_signal.emit()

    def prev_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.procedureStack.setCurrentIndex(self.current_index)
            self.button_group.button(self.current_index).setChecked(True)  # Update radio button
            self.page_changed_signal.emit()