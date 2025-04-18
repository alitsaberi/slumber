from enum import Enum

from loguru import logger
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
)
from screen_brightness_control import get_brightness, set_brightness

from slumber import settings

from .widget_ui import Ui_SleepPage

SCREEN_DIM_TIMEOUT = settings["gui"]["screen_dim_timeout"]
SCREEN_DIM_BRIGHTNESS = settings["gui"]["screen_dim_brightness"]


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

        # Add screen dimming timer
        self.dim_timer = QTimer(self)
        self.original_brightness = None
        self.is_asleep = False

        # Install event filter to detect user interaction
        self.installEventFilter(self)

        self.status_label.setText(f"{State.Awake.value}")
        self.sleep_button.setText(f"{ButtonLabel.SLEEPING.value}")
        self.awake_button.setText(f"{ButtonLabel.Awake.value}")

        self.awake_button.hide()  # Start hidden

        self._connect_signals()

    def _connect_signals(self):
        self.sleep_button.clicked.connect(self._handle_sleep)
        self.awake_button.clicked.connect(self._handle_awake)
        self.end_button.clicked.connect(self._handle_end)
        self.dim_timer.timeout.connect(self._dim_screen)

    def eventFilter(self, obj, event):
        # Reset screen brightness on any user interaction when asleep
        if self.is_asleep and event.type() in [
            Qt.MouseButtonPress.value,
            Qt.KeyPress.value,
        ]:
            self._reset_screen_brightness()
            self.dim_timer.start(SCREEN_DIM_TIMEOUT)
        return super().eventFilter(obj, event)

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
        # Start the dim timer when going to sleep
        self.dim_timer.start(SCREEN_DIM_TIMEOUT)

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
            # Stop timer and ensure screen is back to normal
            self.dim_timer.stop()
            self._reset_screen_brightness()

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

    def _dim_screen(self):
        self.original_brightness = get_brightness()
        try:
            set_brightness(SCREEN_DIM_BRIGHTNESS)
        except Exception as e:
            logger.error(f"Error setting screen brightness: {e}")

    def _reset_screen_brightness(self):
        if self.original_brightness is None:
            logger.warning("No original brightness to reset to")
            return

        try:
            set_brightness(self.original_brightness)
        except Exception as e:
            logger.error(f"Error resetting screen brightness: {e}")
