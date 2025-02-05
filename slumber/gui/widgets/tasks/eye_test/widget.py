from dataclasses import asdict
from enum import Enum

import numpy as np
from loguru import logger
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtWidgets import QDialog, QWidget

from slumber.dag.units.eye_movement_detection import Settings
from slumber.gui.widgets.tasks.base import TaskPage
from slumber.processing.eye_movement import detect_lr_eye_movements
from slumber.sources.zmax import SAMPLE_RATE, DataType, ZMax
from slumber.utils.data import Data

from .widget_ui import Ui_EyeTestPage


class Status(Enum):
    TEST_STARTED = (
        "Test started. Click the button to end.",
        "color: #2196F3; font-weight: bold; padding: 10px;",
    )
    TEST_ENDED = (
        "Test ended. Detecting eye movements...",
        "color: #2196F3; font-weight: bold; padding: 10px;",
    )
    MOVEMENT_DETECTED = (
        "✅ Eye movements detected!",
        "color: #4CAF50; font-weight: bold; padding: 10px;",
    )
    MOVEMENT_NOT_DETECTED = (
        "❌ No eye movements detected. Please try again.",
        "color: #F44336; font-weight: bold; padding: 10px;",
    )
    DATA_COLLECTION_FAILURE = (
        "❌ Failed to collect data. Please try again.",
        "color: #F44336; font-weight: bold; padding: 10px;",
    )


EEG_DATA_TYPE = [DataType.EEG_LEFT, DataType.EEG_RIGHT]


class ButtonText(Enum):
    START = "Start Test"
    STOP = "End Test"


class DataCollectionThread(QThread):
    data_received = Signal(np.ndarray)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()
        self.is_collecting_data = False

    def run(self):
        self.is_collecting_data = True
        try:
            with ZMax() as zmax:
                while self.is_collecting_data:
                    data = zmax.read(data_types=EEG_DATA_TYPE)
                    self.data_received.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))


class EyeTestPage(TaskPage, Ui_EyeTestPage):
    def __init__(
        self,
        index: int,
        title: str,
        accepted_eye_signals: list[str],
        max_test_duration: float,
        parent: QWidget | None = None,
        **eye_movement_detection_kwargs,
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.index = index
        self.title.setText(title)

        self._accepted_eye_signals = accepted_eye_signals
        self._max_test_duration = max_test_duration
        self._eye_movement_detection_settings = Settings.model_validate(
            {
                "left_eeg_label": DataType.EEG_LEFT.name,
                "right_eeg_label": DataType.EEG_RIGHT.name,
                **eye_movement_detection_kwargs,
            }
        )
        logger.debug(self._eye_movement_detection_settings)

        self.info_dialog = self._init_info_dialog()
        self.test_data = []
        self.collection_thread = DataCollectionThread()
        self.timer = QTimer()
        
        self._connect_signals()
        
    def cleanup(self) -> None:
        if self.collection_thread.isRunning():
            self.collection_thread.is_collecting_data = False
            self.collection_thread.wait()

    def _connect_signals(self) -> None:
        self.test_button.clicked.connect(self._on_test_button_click)
        self.collection_thread.data_received.connect(self._handle_data)
        self.collection_thread.error_occurred.connect(self._handle_error)
        self.timer.timeout.connect(self._end_test)

    def _update_status(self, status: Enum) -> None:
        self.status_label.setText(status.value[0])
        self.status_label.setStyleSheet(status.value[1])

    def _on_test_button_click(self) -> None:
        logger.info("Test button clicked")
        if self.collection_thread.isRunning():
            self._end_test()
        else:
            self._start_test()

    def _start_test(self) -> None:
        logger.info("Starting eye test")
        self.test_button.setText(ButtonText.STOP.value)
        self._update_status(Status.TEST_STARTED)
        self.test_data = []
        self.collection_thread.start()
        self.timer.start(self._max_test_duration * 1000)

    def _end_test(self) -> None:
        logger.info("Ending eye test")
        self.collection_thread.is_collecting_data = False
        self.collection_thread.wait()
        self.test_button.setText(ButtonText.START.value)
        self._update_status(Status.TEST_ENDED)
        self._detect_eye_movements()

    def _handle_data(self, data: np.ndarray) -> None:
        self.test_data.append(data)

    def _handle_error(self, error_msg):
        logger.error(f"Error during eye test: {error_msg}")
        self._update_status(Status.DATA_COLLECTION_FAILURE)
        self.test_button.setText(ButtonText.START.value)

    def _detect_eye_movements(self) -> None:
        data = Data(
            array=np.array(self.test_data),
            channel_names=[data_type.name for data_type in EEG_DATA_TYPE],
            sample_rate=SAMPLE_RATE,
        )
        events = detect_lr_eye_movements(
            data, **asdict(self._eye_movement_detection_settings)
        )
        logger.debug(f"Eye movements event: {events}")
        detected = any(
            event.label.startswith(prefix)
            for event in events
            for prefix in self._accepted_eye_signals
        )

        if detected:
            logger.info("Eye movements detected!")
            self._update_status(Status.MOVEMENT_DETECTED)
            self.done()
        else:
            logger.info("No eye movements detected.")
            self._update_status(Status.MOVEMENT_NOT_DETECTED)

    def _init_info_dialog(self) -> QDialog:
        from .info_ui import Ui_InfoDialog

        dialog = QDialog(self)
        Ui_InfoDialog().setupUi(dialog)
        return dialog
