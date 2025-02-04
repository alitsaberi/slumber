from pathlib import Path

from loguru import logger
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QDialog, QWidget

from slumber.gui.widgets.tasks.base import TaskPage
from slumber.scripts.run_session import LOGS_DIR_NAME
from slumber.sources.zmax import ConnectionClosedError, HDServerAlreadyRunningError, ZMax, open_server

from .widget_ui import Ui_ZMaxConnectionPage

ATTEMPTING_CONNECTION = "Attempting to connect..."
CONNECTED_SUCCESS = "✅ Connected to EEG headband successfully!"
CONNECTED_FAILURE = "❌ Failed to connect to EEG headband."

COLOR_ATTEMPTING = "color: #FFC107; font-weight: bold; padding: 10px;"
COLOR_SUCCESS = "color: #4CAF50; font-weight: bold; padding: 10px;"
COLOR_FAILURE = "color: #F44336; font-weight: bold; padding: 10px;"

BUTTON_DISABLED_STYLE = """
    background-color: #B0BEC5;
    color: white;
    font-weight: bold;
    padding: 10px;
    border-radius: 5px;
"""
BUTTON_ENABLED_STYLE = """
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4CAF50, stop:1 #2E7D32);
    color: white;
    font-weight: bold;
    padding: 10px;
    border-radius: 5px;
"""

HDSERVER_LOG_FILE_NAME = "hdserver.log"


class ConnectThread(QThread):
    """Thread for handling EEG server connection attempts."""

    connected = Signal(bool)
    process_created = Signal(object)

    def run(self) -> None:
        try:
            hdserver = open_server(Path.cwd() / LOGS_DIR_NAME / HDSERVER_LOG_FILE_NAME)
            self.process_created.emit(hdserver)
        except (FileNotFoundError, PermissionError, OSError) as e:
            logger.error(f"Failed to open HDServer: {e}")
            self.connected.emit(False)
            return
        except HDServerAlreadyRunningError as e:
            logger.debug(e)
        
        try:
            with ZMax() as zmax:
                zmax.read()
                self.connected.emit(True)
                return
        except TimeoutError as e:
            logger.debug(e)
            self.connected.emit(False)
            return
        except (ConnectionError, ConnectionClosedError) as e:
            logger.error(e)
            self.connected.emit(False)
            return


class ZMaxConnectionPage(TaskPage, Ui_ZMaxConnectionPage):
    def __init__(self, index: int, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.index = index
        self.title.setText(title)
        self.info_dialog = self._init_info_dialog()
        self.connect_thread = ConnectThread()

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.connect_button.clicked.connect(self.on_connect)
        self.info_button.clicked.connect(self.open_info_dialog)
        self.connect_thread.connected.connect(self.on_connected)
        self.connect_thread.process_created.connect(
            self.window().store_hdserver_process
        )

    def on_connect(self) -> None:
        logger.info("Connect button clicked")
        self.status_label.setText(ATTEMPTING_CONNECTION)
        self.status_label.setStyleSheet(COLOR_ATTEMPTING)

        self.connect_button.setEnabled(False)
        self.connect_button.setStyleSheet(BUTTON_DISABLED_STYLE)

        self.connect_thread.start()

    def on_connected(self, success: bool) -> None:
        if success:
            self.status_label.setText(CONNECTED_SUCCESS)
            self.status_label.setStyleSheet(COLOR_SUCCESS)
            self.done()
        else:
            self.status_label.setText(CONNECTED_FAILURE)
            self.status_label.setStyleSheet(COLOR_FAILURE)

            # Re-enable button and restore style
            self.connect_button.setEnabled(True)
            self.connect_button.setStyleSheet(BUTTON_ENABLED_STYLE)

    def _init_info_dialog(self) -> QDialog:
        from .info_ui import Ui_InfoDialog

        dialog = QDialog(self)
        ui = Ui_InfoDialog()
        ui.setupUi(dialog)
        return dialog

    def open_info_dialog(self) -> None:
        logger.info("Opening info dialog")
        self.info_dialog.exec()
