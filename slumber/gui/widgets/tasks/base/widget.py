from loguru import logger
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget

from .help_ui import Ui_HelpDialog
from .widget_ui import Ui_TaskPage


class TaskPage(QWidget, Ui_TaskPage):
    done_signal = Signal(int)

    def __init__(self, index: int, title: str, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.index = index
        self.title.setText(title)
        self.info_dialog = self._init_info_dialog()
        self.info_button.clicked.connect(self.open_info_dialog)

        # Delete this button if done button is deleted
        self.done_button.clicked.connect(self.done)

    def _init_info_dialog(self) -> QDialog:
        dialog = QDialog(self)
        ui = Ui_HelpDialog()
        ui.setupUi(dialog)
        return dialog
    
    def open_info_dialog(self) -> None:
        logger.info("Opening info dialog")
        self.info_dialog.exec()

    def done(self) -> None:
        logger.info(f"Task {self.title} is done")
        self.done_signal.emit(self.index)
