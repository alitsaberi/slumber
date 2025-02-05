from enum import Enum

from loguru import logger
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QPushButton, QWidget

from slumber.dag.units.home_lucid_dreaming.cueing import CueIntensityConfig
from slumber.dag.units.zmax import ZMaxStimulationSignal
from slumber.gui.widgets.tasks.base import TaskPage
from slumber.sources.zmax import ZMax

from .widget_ui import Ui_LightCueCalibrationPage


class Status(Enum):
    TO_START_CUEING = (
        "Ready to start cueing.\nAdjust intensity if needed and click `Present Cue`.",
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
    CONFIRMED = (
        "✅ Light cue perceived!",
        "color: #4CAF50; font-weight: bold; padding: 10px;",
    )


class ButtonStyle(Enum):
    DISABLED = """
        background-color: #B0BEC5;
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
    """
    ENABLED = """
        background: qlineargradient(x1:0, y1:0, x2:1, 
            y2:1, stop:0 #4CAF50, stop:1 #2E7D32);
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
    """


def set_button_enabled(button: QPushButton, enabled: bool) -> None:
    button.setEnabled(enabled)
    style = ButtonStyle.ENABLED if enabled else ButtonStyle.DISABLED
    button.setStyleSheet(style.value)


class LightCueCalibrationPage(TaskPage, Ui_LightCueCalibrationPage):
    def __init__(
        self,
        index: int,
        title: str,
        min: int,
        max: int,
        step: int,
        led_color: str,
        repetitions: int,
        on_duration: int,
        off_duration: int,
        alternate_eyes: bool,
        countdown_seconds: int,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.index = index
        self.title.setText(title)

        self.cue_intensity_config = CueIntensityConfig(
            value=min,
            min=min,
            max=max,
            step=step,
        )
        self.stimulation_signal = ZMaxStimulationSignal(
            led_color=led_color,
            repetitions=repetitions,
            on_duration=on_duration,
            off_duration=off_duration,
            vibration=False,
            led_intensity=self.cue_intensity_config.value,
            alternate_eyes=alternate_eyes,
        )
        self.zmax = ZMax()
        self.countdown_seconds = countdown_seconds

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._update_countdown)

        self._update_status(Status.TO_START_CUEING)
        self._update_intensity_layout()
        self._set_perception_widget_visible(False)

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.cue_button.clicked.connect(self._on_cue_button_click)
        self.increase_intensity_button.clicked.connect(self._increase_intensity)
        self.decrease_intensity_button.clicked.connect(self._decrease_intensity)
        self.yes_button.clicked.connect(self._confirm_perception)
        self.no_button.clicked.connect(self._retry)

    def _update_status(self, status: Enum) -> None:
        logger.info(f"Updating status to {status}")
        self.status_label.setText(status.value[0])
        self.status_label.setStyleSheet(status.value[1])

    def _update_intensity_layout(self) -> None:
        logger.info(f"Updating intensity layout: {self.cue_intensity_config}")
        self.intensity_display.display(self.cue_intensity_config.value)
        set_button_enabled(
            self.decrease_intensity_button,
            self.cue_intensity_config.value > self.cue_intensity_config.min,
        )
        set_button_enabled(
            self.increase_intensity_button,
            self.cue_intensity_config.value < self.cue_intensity_config.max,
        )

    def _set_perception_widget_visible(self, visible: bool) -> None:
        logger.info(
            f"Setting perception widget visible: {visible}",
            is_visible=self.perception_widget.isVisible(),
        )
        self.perception_widget.setVisible(visible)

    def _set_buttons_enabled(self, enabled: bool) -> None:
        logger.info(f"Setting buttons enabled: {enabled}")
        set_button_enabled(self.cue_button, enabled)
        set_button_enabled(self.increase_intensity_button, enabled)
        set_button_enabled(self.decrease_intensity_button, enabled)

        if enabled:
            self._update_intensity_layout()

    def _on_cue_button_click(self) -> None:
        logger.info("Cue button clicked")
        self._update_status(Status.CUEING)
        self._set_buttons_enabled(False)
        self.remaining_seconds = self.countdown_seconds
        self._update_countdown()
        self.timer.start()

    def _update_countdown(self) -> None:
        self.intensity_display.display(self.remaining_seconds)
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
        else:
            self.timer.stop()
            self._deliver_cue()
            self._update_intensity_layout()
            self._set_buttons_enabled(False)

    def _deliver_cue(self) -> None:
        logger.info(f"Delivering cue: {self.stimulation_signal}")
        try:
            self.zmax.connect()
            self.zmax.stimulate(**self.stimulation_signal.model_dump())
            logger.info("Cue delivered", stimulation_signal=self.stimulation_signal)
            self._update_status(Status.CUED)
            self._set_perception_widget_visible(True)
        except Exception as e:
            logger.error(f"Error delivering light cue: {e}")
            self._update_status(Status.FAILURE)
            self._set_buttons_enabled(True)

    def _increase_intensity(self) -> None:
        self._adjust_intensity(True)

    def _decrease_intensity(self) -> None:
        self._adjust_intensity(False)

    def _adjust_intensity(self, increase: bool) -> None:
        self.cue_intensity_config.adjust(increase)
        self.stimulation_signal.led_intensity = self.cue_intensity_config.value
        self._update_intensity_layout()

    def _confirm_perception(self) -> None:
        logger.info("Perception confirmed by participant.")
        self._set_perception_widget_visible(False)
        self._update_status(Status.CONFIRMED)

        # TODO: Store intensity

        self.done()

    def _retry(self) -> None:
        logger.info("Participant did not perceive the cue.")
        self._set_perception_widget_visible(False)
        self._update_status(Status.TO_START_CUEING)
        self._set_buttons_enabled(True)

    def _init_info_dialog(self) -> QDialog:
        from .info_ui import Ui_InfoDialog

        dialog = QDialog(self)
        Ui_InfoDialog().setupUi(dialog)
        return dialog
