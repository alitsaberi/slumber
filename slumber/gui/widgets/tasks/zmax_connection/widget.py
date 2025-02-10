from enum import Enum

from loguru import logger
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QDialog, QWidget

from slumber import settings
from slumber.gui.widgets.tasks.base import TaskPage
from slumber.sources.zmax import (
    DataType,
    ZMax,
    voltage_to_percentage,
)

from .widget_ui import Ui_ZMaxConnectionPage


class Status(Enum):
    ATTEMPTING = (
        "Attempting to connect...",
        "color: #FFC107; font-weight: bold; padding: 10px;",
    )
    SUCCESS = (
        "✅ Connected | ✅ Battery level is sufficient.",
        "color: #4CAF50; font-weight: bold; padding: 10px;",
    )
    FAILURE = (
        "❌ Failed to connect to EEG headband.",
        "color: #F44336; font-weight: bold; padding: 10px;",
    )
    BATTERY_LOW = (
        "✅ Connected | ⚠ Battery low! Please charge and try again.",
        "color: #FF9800; font-weight: bold; padding: 10px;",
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


class ConnectThread(QThread):
    connected = Signal(bool)

    def run(self) -> None:
        try:
            with ZMax() as zmax:
                zmax.read()  # Ensure connection is established
                self.connected.emit(True)
        except Exception as e:
            logger.error(f"ZMax connection error: {e}")
            self.connected.emit(False)


class ZMaxConnectionPage(TaskPage, Ui_ZMaxConnectionPage):
    def __init__(self, index: int, title: str, battery_level_threshold: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.index = index
        self.title.setText(title)
        
        self.battery_level_threshold = battery_level_threshold

        self.info_dialog = self._init_info_dialog()
        self.connect_thread = ConnectThread()

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.connect_button.clicked.connect(self._on_connect)
        self.info_button.clicked.connect(self.info_dialog.exec)
        self.connect_thread.connected.connect(self._on_connected)

    def _on_connect(self) -> None:
        self._update_status(Status.ATTEMPTING)
        self._toggle_button(False)
        self.connect_thread.start()

    def _on_connected(self, success: bool) -> None:
        if success:
            self._handle_successful_connection()
        else:
            self._handle_failed_connection()

    def _handle_successful_connection(self) -> None:
        try:
            with ZMax() as zmax:
                battery_voltage = zmax.read(data_types=[DataType.BATTERY])[0]
                battery_percentage = voltage_to_percentage(battery_voltage)
                self._check_battery_level(battery_percentage)
        except Exception as e:
            logger.error(f"Battery check error: {e}")
            self._handle_failed_connection()

    def _handle_failed_connection(self) -> None:
        self._update_status(Status.FAILURE)
        self._toggle_button(True)

    def _check_battery_level(self, battery_level: int) -> None:
        self.battery_led.display(battery_level)
        if battery_level >= self.battery_level_threshold:
            self._update_status(Status.SUCCESS)
            self._toggle_button(False)
            self.done()
        else:
            self._update_status(Status.BATTERY_LOW)
            self._toggle_button(True)

    def _update_status(self, status: Enum) -> None:
        self.status_label.setText(status.value[0])
        self.status_label.setStyleSheet(status.value[1])

    def _toggle_button(self, enabled: bool) -> None:
        self.connect_button.setEnabled(enabled)
        style = ButtonStyle.ENABLED if enabled else ButtonStyle.DISABLED
        self.connect_button.setStyleSheet(style.value)

    def _init_info_dialog(self) -> QDialog:
        from .info_ui import Ui_InfoDialog

        dialog = QDialog(self)
        Ui_InfoDialog().setupUi(dialog)
        return dialog
