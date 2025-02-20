from enum import Enum
from pathlib import Path

from loguru import logger
from pydantic import TypeAdapter
from PySide6.QtCore import QTimer
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

        self.protocol = TypeAdapter(Protocol).validate_python(
            load_yaml(self.protocol_path)
        )

        self.countdown_seconds = countdown_seconds
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._update_countdown)
        self.engine = init_text2speech_engine(
            rate=rate,
            volume=MAX_VOLUME,
            voice=voice,
        )

        self._init_status()
        self._connect_signals()

    def _init_status(self) -> None:
        logger.info("Initializing the status")
        self._update_status(Status.TO_START)
        set_button_enabled(self.start_button, True)

    def _connect_signals(self) -> None:
        self.start_button.clicked.connect(self._on_start_button_click)

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
        logger.info("Starting training")
        try:
            with ZMax() as zmax:
                training_config = CognitiveTrainingConfig(
                    zmax=zmax,
                    text2speech_engine=self.engine,
                    min_subjective_light_intensity=self.window().minimum_subjective_light_intensity,
                    minimum_subjective_audio_intensity=self.window().minimum_subjective_audio_intensity,
                )

                logger.info(f"Starting training: {training_config}")

                execute_cognitive_training(
                    protocol=self.protocol,
                    config=training_config,
                )

            logger.info("Training completed successfully")
            self._update_status(Status.SUCCESS)
            self.done()
            self.parent().parent().done_signal.emit()
            self.window().sleep_page.go_to_sleep()
        except Exception as e:
            logger.error(f"Training failed: {e}")
            self._update_status(Status.FAILURE)
