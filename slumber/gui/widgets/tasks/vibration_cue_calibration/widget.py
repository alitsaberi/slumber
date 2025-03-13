from enum import Enum

from loguru import logger
from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import QMessageBox, QPushButton, QWidget

from slumber.dag.units.zmax import ZMaxStimulationSignal
from slumber.gui.widgets.tasks.base import TaskPage
from slumber.sources.zmax import LEDColor, ZMax

from .widget_ui import Ui_VibrationCueCalibrationPage


class Status(Enum):
    TO_START_CUEING = (
        "Ready to start cueing. Click `Present Cue` to start.",
        "color: #2196F3; font-weight: bold; padding: 10px;",
    )
    CUEING = (
        "Delivering cue in...",
        "color: #FFC107; font-weight: bold; padding: 10px;",
    )
    CUED = (
        "Cue delivered!",
        "color: #FFC107; font-weight: bold; padding: 10px;",
    )
    FAILURE = (
        "❌ Failed to deliver light cue. Please try again.",
        "color: #F44336; font-weight: bold; padding: 10px;",
    )
    SUCCESS = (
        "✅ Calibration successful!",
        "color: #4CAF50; font-weight: bold; padding: 10px;",
    )


class ButtonStyle(Enum):
    DISABLED = """
        background-color: #B0BEC5;
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 25px;
    """
    ENABLED = """
        background: qlineargradient(x1:0, y1:0, x2:1, 
            y2:1, stop:0 #4CAF50, stop:1 #2E7D32);
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 25px;
    """


PERCEPTION_QUESTION_BOX_TITLE = "Perception"
PERCEPTION_QUESTION = "Did you perceive the vibration cue?"


def set_button_enabled(button: QPushButton, enabled: bool) -> None:
    button.setEnabled(enabled)
    style = ButtonStyle.ENABLED if enabled else ButtonStyle.DISABLED
    button.setStyleSheet(style.value)


class CueDeliveryThread(QThread):
    cue_delivered = Signal(bool)

    def __init__(self, stimulation_signal: ZMaxStimulationSignal):
        super().__init__()
        self.stimulation_signal = stimulation_signal
        self.zmax = ZMax()

    def run(self) -> None:
        logger.info(f"Delivering cue: {self.stimulation_signal}")
        try:
            self.zmax.connect()
            self.zmax.stimulate(**self.stimulation_signal.model_dump())
            self.cue_delivered.emit(True)
        except Exception as e:
            logger.exception(f"Error delivering light cue: {e}")
            self.cue_delivered.emit(False)


class VibrationCueCalibrationPage(TaskPage, Ui_VibrationCueCalibrationPage):
    def __init__(
        self,
        index: int,
        title: str,
        on_duration: int,
        off_duration: int,
        repetitions: int,
        countdown_seconds: int,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(index, title, parent=parent)

        self.cue_thread = CueDeliveryThread(
            ZMaxStimulationSignal(
                vibration=True,
                led_color=LEDColor.OFF,
                repetitions=repetitions,
                on_duration=on_duration,
                off_duration=off_duration,
            )
        )

        self.countdown_seconds = countdown_seconds
        self.timer = QTimer()
        self.timer.setInterval(1000)

        self._init_status()
        self._connect_signals()

    def _init_status(self) -> None:
        logger.info("Initializing cueing state")
        self._update_status(Status.TO_START_CUEING)
        set_button_enabled(self.cue_button, True)

    def _connect_signals(self) -> None:
        self.cue_button.clicked.connect(self._on_cue_button_click)
        self.timer.timeout.connect(self._update_countdown)
        self.cue_thread.cue_delivered.connect(self._handle_cue_delivery)

    def _update_status(self, status: Enum) -> None:
        logger.info(f"Updating status to {status}")
        self.status_label.setText(status.value[0])
        self.status_label.setStyleSheet(status.value[1])

    def _on_cue_button_click(self) -> None:
        logger.info("Cue button clicked")
        self._update_status(Status.CUEING)
        set_button_enabled(self.cue_button, False)
        self.remaining_seconds = self.countdown_seconds
        self._update_countdown()
        self.timer.start()

    def _update_countdown(self) -> None:
        self.timer_display.display(self.remaining_seconds)
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
        else:
            self.timer.stop()
            self._deliver_cue()

    def _deliver_cue(self) -> None:
        logger.info("Starting cue delivery thread")
        self.cue_thread.start()

    def _handle_cue_delivery(self, success: bool) -> None:
        if success:
            self._update_status(Status.CUED)
            self._show_perception_question()
        else:
            self._update_status(Status.FAILURE)
            set_button_enabled(self.cue_button, True)

    def _show_perception_question(self):
        logger.info("Showing perception question")
        reply = QMessageBox.question(
            self,
            PERCEPTION_QUESTION_BOX_TITLE,
            PERCEPTION_QUESTION,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        logger.info(
            f"Perception question reply: {'yes' if reply == QMessageBox.Yes else 'no'}"
        )

        if reply == QMessageBox.Yes:
            self._finish_calibration()
            return

        self._init_status()

    def _finish_calibration(self) -> None:
        logger.info("Finishing calibration")
        self._update_status(Status.SUCCESS)
        self.done()

    def cleanup(self):
        logger.info("Cleaning up...")
        self.cue_thread.zmax.disconnect()
        if self.cue_thread.isRunning():
            self.cue_thread.quit()
            self.cue_thread.wait()
