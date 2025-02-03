import typing

from loguru import logger
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QListWidgetItem,
    QWidget,
)

if typing.TYPE_CHECKING:
    from slumber.dag.units.gui import Procedure, Task

from .widget_ui import Ui_ProcedurePage

INITIAL_INDEX = 0
TASK_TITLE_FORMAT = "{index}. {title}"


def _set_item_enabled(item: QListWidgetItem, enabled: bool) -> None:
    flags = item.flags()
    if enabled:
        flags |= Qt.ItemIsEnabled
    else:
        flags &= ~Qt.ItemIsEnabled
    item.setFlags(flags)


class ProcedurePage(QWidget, Ui_ProcedurePage):
    done_signal = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class
        self._connect_signals()
        self.procedure = None

    @property
    def current_index(self) -> int:
        return self.stacked_widget.currentIndex()

    @property
    def n_tasks(self) -> int:
        return self.procedure.n_tasks

    def set_procedure(self, procedure: "Procedure") -> None:
        if not procedure.tasks:
            raise ValueError("Tasks list is empty")

        self.procedure = procedure
        self._clear_widgets()
        self._load_tasks()
        self._open_task(INITIAL_INDEX)
        self.done_button.setEnabled(False)

    def reset_procedure(self) -> None:
        self.set_procedure(self.procedure)

    def is_on_first_task(self) -> bool:
        return self.current_index == INITIAL_INDEX

    def is_on_last_task(self) -> bool:
        return self.current_index == self.n_tasks - 1

    def _connect_signals(self) -> None:
        self.next_button.clicked.connect(self._open_next_task)
        self.previous_button.clicked.connect(self._open_previous_task)
        self.task_list.itemClicked.connect(self._handle_item_click)
        self.done_button.clicked.connect(self._on_done_button_clicked)

    def _load_tasks(self) -> None:
        logger.info(f"Loading {self.n_tasks} tasks")
        for idx, task in enumerate(self.procedure.tasks):
            title = f"{idx + 1}. {task.title}"
            self._add_task_item(idx, title)
            self._add_task_page(task, idx, title, **task.kwargs)

    def _clear_widgets(self) -> None:
        self.task_list.clear()
        while self.stacked_widget.count() > 0:
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()

    def _add_task_item(self, idx: int, title: str) -> None:
        item = QListWidgetItem()
        item.setText(title)
        item.setCheckState(Qt.CheckState.Unchecked)
        _set_item_enabled(item, idx == INITIAL_INDEX)
        self.task_list.addItem(item)

    def _add_task_page(self, task: "Task", idx: int, title: str, **kwargs) -> None:
        logger.info(f"Adding task {idx + 1} - {task} to the list")
        task_page = task.widget(idx, title, **kwargs, parent=self)
        task_page.done_signal.connect(self._on_task_done)
        self.stacked_widget.addWidget(task_page)

    def _on_task_done(self, index: int):
        item = self.task_list.item(index)
        item.setCheckState(Qt.Checked)

        if not self.is_on_last_task():
            next_item = self.task_list.item(index + 1)
            _set_item_enabled(next_item, True)
            self._update_navigation_buttons()
        else:
            self.done_button.setEnabled(True)

    def _open_next_task(self) -> None:
        self._open_task(self.current_index + 1)

    def _open_previous_task(self):
        self._open_task(self.current_index - 1)

    def _open_task(self, index: int) -> None:
        logger.info(f"Navigating to page {index}")
        self.stacked_widget.setCurrentIndex(index)
        self.task_list.setCurrentRow(index)
        self._update_navigation_buttons()

    def _update_navigation_buttons(self):
        self.previous_button.setEnabled(not self.is_on_first_task())
        self.next_button.setEnabled(
            self.task_list.item(self.current_index).checkState() == Qt.Checked
            and not self.is_on_last_task()
        )

    def _on_done_button_clicked(self):
        logger.info("Done button clicked")
        self.done_signal.emit()

    def _handle_item_click(self, item: QListWidgetItem) -> None:
        if item.flags() & Qt.ItemIsEnabled:
            index = self.task_list.row(item)
            self._open_task(index)
