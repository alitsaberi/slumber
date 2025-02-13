from PySide6.QtWidgets import QWidget

from slumber.gui.widgets.tasks.base import TaskPage

from .widget_ui import Ui_EmptyPage


class EmptyPage(TaskPage, Ui_EmptyPage):
    def __init__(self, index: int, title: str, parent: QWidget = None):
        super().__init__(index, title, parent=parent)

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.done_button.clicked.connect(self.done)
