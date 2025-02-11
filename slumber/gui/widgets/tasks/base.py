from loguru import logger
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class TaskPage(QWidget):
    done_signal = Signal(int)

    def done(self) -> None:
        logger.info(f"Task {self.title.text()} is done")
        self.done_signal.emit(self.index)
