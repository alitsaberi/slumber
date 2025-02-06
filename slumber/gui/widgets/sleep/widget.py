from enum import Enum

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
)

from .widget_ui import Ui_SleepPage


class State(Enum):
    Awake = "Awake 🌞"
    Asleep = "Asleep 😴"


class SleepPage(QWidget, Ui_SleepPage):
    state_changed = Signal(State)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setupUi(self)

        self.state = State.Awake
        self.status_label.setText(f"{State.Awake.value}")
        self.sleep_button.clicked.connect(self.handle_sleep)
        self.awake_button.clicked.connect(self.handle_awake)

        self.awake_button.hide()  # Start hidden

    def handle_sleep(self):
        reply = QMessageBox.question(
            self,
            "Confirm Sleep",
            "Are you ready to go to sleep?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.is_asleep = True
            self.sleep_button.hide()
            self.awake_button.show()
            self.update_state(State.Asleep)

    def handle_awake(self):
        reply = QMessageBox.question(
            self,
            "Confirm Wake-Up",
            "Are you sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.is_asleep = False
            self.awake_button.hide()
            self.sleep_button.show()
            self.update_state(State.Awake)

    def update_state(self, state: State) -> None:
        self.state = state
        self.status_label.setText(f"{state.value}")
        self.state_changed.emit(state)
