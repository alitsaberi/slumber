from loguru import logger
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QWidget


class TaskPage(QWidget):
    done_signal = Signal(int)

    def __init__(
        self,
        index: int,
        title: str,
        has_info: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.index = index

        self.title.setText(title)

        if not has_info:
            self.info_button.hide()

    def done(self) -> None:
        logger.info(f"Task {self.title.text()} is done")
        self.done_signal.emit(self.index)

    def _init_info_dialog(self) -> QDialog:
        from .info_ui import Ui_InfoDialog  # type: ignore

        dialog = QDialog(self)
        ui = Ui_InfoDialog()
        ui.setupUi(dialog)
        return dialog
