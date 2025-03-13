from enum import Enum
from pathlib import Path

from loguru import logger
from pydantic import TypeAdapter
from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import QPushButton, QWidget

from slumber.gui.widgets.tasks.base import TaskPage
from slumber.sources.zmax import ZMax
from slumber.tasks.cognitive_training import (
    CognitiveTrainingConfig,
    Protocol,
    execute_cognitive_training,
)
from slumber.utils.helpers import load_yaml
from slumber.utils.text2speech import MAX_VOLUME, init_text2speech_engine

from .widget_ui import Ui_CognitiveTrainingPage

GO_TO_SLEEP_DELAY = 10000


class Status(Enum):
    TO_START = (
        "Ready to start the training. Click `Start`.",
        "color: #2196F3; font-weight: bold; padding: 10px;",
    )
    STARTING = (
        "Starting the training in ...",
        "color: #FFC107; font-weight: bold; padding: 10px;",
    )
    IN_PROGRESS = (
        "Training in progress.",
        "color: #FFC107; font-weight: bold; padding: 10px;",
    )
    FAILURE = (
        "❌ Failed to complete the training. Please try again.",
        "color: #F44336; font-weight: bold; padding: 10px;",
    )
    SUCCESS = (
        "✅ Training completed successfully!",
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


def set_button_enabled(button: QPushButton, enabled: bool) -> None:
    button.setEnabled(enabled)
    style = ButtonStyle.ENABLED if enabled else ButtonStyle.DISABLED
    button.setStyleSheet(style.value)


class TrainingThread(QThread):
    training_completed = Signal(bool)

    def __init__(self, protocol: Protocol, config: CognitiveTrainingConfig):
        super().__init__()
        self.protocol = protocol
        self.config = config

    def run(self) -> None:
        logger.info("Starting training...")
        try:
            self.config.zmax.connect()
            execute_cognitive_training(
                protocol=self.protocol,
                config=self.config,
            )
            self.training_completed.emit(True)
        except Exception as e:
            logger.exception(f"Error during training: {e}")
            self.training_completed.emit(False)


class CognitiveTrainingPage(TaskPage, Ui_CognitiveTrainingPage):
    def __init__(
        self,
        index: int,
        title: str,
        protocol_path: Path | str,
        rate: int,
        voice: str,
        countdown_seconds: int,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(index, title, parent=parent)

        self.protocol_path = Path(protocol_path).absolute()
        if not self.protocol_path.exists():
            raise FileNotFoundError(f"Protocol file not found: {self.protocol_path}")

        self.zmax = ZMax()
        self.engine = init_text2speech_engine(
            rate=rate,
            volume=MAX_VOLUME,
            voice=voice,
        )

        self.training_thread = TrainingThread(
            protocol=TypeAdapter(Protocol).validate_python(
                load_yaml(self.protocol_path)
            ),
            config=CognitiveTrainingConfig(
                zmax=self.zmax,
                text2speech_engine=self.engine,
                min_subjective_light_intensity=self.window().minimum_subjective_light_intensity,
                minimum_subjective_audio_intensity=self.window().minimum_subjective_audio_intensity,
            ),
        )

        self.countdown_seconds = countdown_seconds
        self.timer = QTimer()
        self.timer.setInterval(1000)

        self._init_status()
        self._connect_signals()

    def _init_status(self) -> None:
        logger.info("Initializing the status")
        self._update_status(Status.TO_START)
        set_button_enabled(self.start_button, True)

    def _connect_signals(self) -> None:
        self.start_button.clicked.connect(self._on_start_button_click)
        self.timer.timeout.connect(self._update_countdown)
        self.training_thread.training_completed.connect(
            self._handle_training_completion
        )

    def _update_status(self, status: Enum) -> None:
        logger.info(f"Updating status to {status}")
        self.status_label.setText(status.value[0])
        self.status_label.setStyleSheet(status.value[1])

    def _on_start_button_click(self) -> None:
        logger.info("Start button clicked")
        self._update_status(Status.STARTING)
        set_button_enabled(self.start_button, False)
        self.remaining_seconds = self.countdown_seconds
        self._update_countdown()
        self.timer.start()

    def _update_countdown(self) -> None:
        self.timer_display.display(self.remaining_seconds)
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
        else:
            self.timer.stop()
            self._update_status(Status.IN_PROGRESS)
            self._start_training()

    def _start_training(self) -> None:
        logger.info("Starting training thread")
        self.training_thread.start()

    def _handle_training_completion(self, success: bool) -> None:
        if success:
            logger.info("Training completed successfully")
            self._update_status(Status.SUCCESS)
            self.done()
            self.parent().parent().done_signal.emit()
            QTimer.singleShot(GO_TO_SLEEP_DELAY, self.window().sleep_page.go_to_sleep)
        else:
            self._update_status(Status.FAILURE)

    def cleanup(self):
        logger.info("Cleaning up...")
        self.zmax.disconnect()
        self.engine.stop()
        if self.training_thread.isRunning():
            self.training_thread.quit()
            self.training_thread.wait()
