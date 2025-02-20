from enum import Enum

from loguru import logger
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
)

from .widget_ui import Ui_SleepPage


class State(Enum):
    Awake = "Awake 🌞"
    Asleep = "Asleep 😴"


class ButtonLabel(Enum):
    Awake = "I'm Awake"
    SLEEPING = "Going to Sleep"


class SleepPage(QWidget, Ui_SleepPage):
    state_changed = Signal(State)
    end_session = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)

        self.status_label.setText(f"{State.Awake.value}")
        self.sleep_button.setText(f"{ButtonLabel.SLEEPING.value}")
        self.awake_button.setText(f"{ButtonLabel.Awake.value}")

        self.awake_button.hide()  # Start hidden

        self._connect_signals()

    def _connect_signals(self):
        self.sleep_button.clicked.connect(self._handle_sleep)
        self.awake_button.clicked.connect(self._handle_awake)
        self.end_button.clicked.connect(self._handle_end)

    def _handle_sleep(self):
        reply = QMessageBox.question(
            self,
            "Confirm Sleep",
            "Are you ready to go to sleep?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.go_to_sleep()

    def go_to_sleep(self) -> None:
        logger.info("Going to sleep")
        self.is_asleep = True
        self.sleep_button.hide()
        self.awake_button.show()
        self._update_state(State.Asleep)

    def _handle_awake(self):
        reply = QMessageBox.question(
            self,
            "Confirm Wake-Up",
            "Are you sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            logger.info("Waking up")
            self.is_asleep = False
            self.awake_button.hide()
            self.sleep_button.show()
            self._update_state(State.Awake)

    def _update_state(self, state: State) -> None:
        self.status_label.setText(f"{state.value}")
        self.state_changed.emit(state)

    def _handle_end(self):
        reply = QMessageBox.question(
            self,
            "Confirm End",
            "Are you sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.end_session.emit()
