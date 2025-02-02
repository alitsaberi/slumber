from loguru import logger
from PySide6.QtWidgets import QDialog, QWidget

from slumber.gui.widgets.tasks.base import TaskPage

from .widget_ui import Ui_EmptyPage


class EmptyPage(TaskPage, Ui_EmptyPage):
    def __init__(self, index: int, title: str, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.index = index
        self.title.setText(title)
        self.info_dialog = self._init_info_dialog()

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.info_button.clicked.connect(self.open_info_dialog)
        self.done_button.clicked.connect(self.done)

    def _init_info_dialog(self) -> QDialog:
        from .info_ui import Ui_InfoDialog

        dialog = QDialog(self)
        ui = Ui_InfoDialog()
        ui.setupUi(dialog)
        return dialog

    def open_info_dialog(self) -> None:
        logger.info("Opening info dialog")
        self.info_dialog.exec()
