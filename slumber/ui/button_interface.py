"""
GUI interface for controlling and interacting with the Zmax server.
Provides connection management, and signal quality check capabilities.
Will be expanded in the future to include actual data recording.
"""

import logging
import sys

import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from slumber import settings
from slumber.data_sources.zmax import DataType, ZMax
from slumber.tasks.evaluate_signal_quality import evaluate_signal_quality

Logger = logging.getLogger("slumber")


class ZmaxDataThread(QThread):
    """
    Background thread for handling Zmax server communication.

    Signals:
        data_received (str): Emitted when new data arrives from server
        connection_status (bool): Emitted when connection state changes
        buffer_complete (list): Emitted when buffer recording finishes

    Attributes:
        buffer_data (list[list[float]]): Temporary storage for signal quality check data
        buffer_size (int): Number of samples to collect for quality check
        host (str): Server hostname or IP address
        port (int): Server port number
        is_running (bool): Thread execution control flag
        is_recording (bool): Recording state control flag
        is_buffer_recording (bool): Buffer recording state flag
    """

    data_received = pyqtSignal(str)  # Signal emitted when new data arrives
    connection_status = pyqtSignal(bool)  # Signal for connection state changes
    buffer_complete = pyqtSignal(list)  # New signal for buffer completion

    def __init__(self) -> None:
        super().__init__()
        self.zmax_socket = None
        self.is_running = False
        self.is_recording = False
        self.is_buffer_recording = False
        self.buffer_data = []
        self.buffer_size = (
            settings["processing"]["sample_rate"]
            * settings["processing"]["signal_quality_check"]["window_duration"]
        )
        self.host = settings["zmax"]["host"]  # Default zmax value from settings
        self.port = settings["zmax"]["port"]  # Default zmax value from settings

    def run(self) -> None:
        """
        Main thread execution loop. Establishes connection with Zmax server and handles
        continuous data reception.

        Emits:
            connection_status: Connection state updates
            data_received: New data from server
            buffer_complete: When buffer recording is finished
        """

        with ZMax(ip=self.host, port=self.port) as zmax_socket:
            zmax_socket.send_string("HELLO\n")  # For some reason this is necessary
            self.connection_status.emit(True)
            self.is_running = True

            while self.is_running:
                if self.is_recording or self.is_buffer_recording:
                    # TODO: use global settings for requested zmax channels
                    data = zmax_socket.read(
                        [
                            DataType.EEG_RIGHT,
                            DataType.EEG_LEFT,
                            DataType.ACCELEROMETER_X,
                            DataType.ACCELEROMETER_Y,
                            DataType.ACCELEROMETER_Z,
                        ]
                    ).tolist()[0]

                    if data == []:  # Check received data not empty
                        continue

                    self.data_received.emit(str(data))

                    if self.is_buffer_recording:
                        self.buffer_data.append(data)
                        if len(self.buffer_data) >= self.buffer_size:
                            self.is_buffer_recording = False
                            self.buffer_complete.emit(self.buffer_data)
                            self.buffer_data = []


class ConnectionPage(QWidget):
    """
    Page widget for configuring and establishing server connections.

    Provides input fields for host/port configuration and connection controls.
    Serves as the initial interface before connecting to the Zmax server.

    Attributes:
        host_input (QLineEdit): Input field for server hostname/IP
        port_input (QLineEdit): Input field for server port
        connect_btn (QPushButton): Button to initiate server connection
    """

    def __init__(self) -> None:
        """Initialize and layout connection page components."""
        super().__init__()
        layout = QVBoxLayout()

        # Connection settings
        self.host_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("8000")
        self.connect_btn = QPushButton("Connect to Server")

        layout.addWidget(QLabel("Host:"))
        layout.addWidget(self.host_input)
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_input)
        layout.addWidget(self.connect_btn)
        layout.addStretch()

        self.setLayout(layout)


class ControlPage(QWidget):
    """
    Page widget for managing active server operations.

    Provides controls for recording management and real-time data monitoring.
    Displays logging output and signal quality status.

    Attributes:
        buffer_record_btn (QPushButton): Initiates signal quality check recording
        toggle_record_btn (QPushButton): Controls main data recording
        clear_btn (QPushButton): Clears the log display
        log_display (QTextEdit): Shows logging output and status messages
    """

    def __init__(self) -> None:
        """Initialize and layout control page components."""
        super().__init__()
        layout = QVBoxLayout()

        # Control buttons
        self.buffer_record_btn = QPushButton("Record Buffer")
        self.toggle_record_btn = QPushButton("Start Recording")
        self.clear_btn = QPushButton("Clear Log")

        # Data display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.buffer_record_btn)
        button_layout.addWidget(self.toggle_record_btn)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)
        layout.addWidget(self.log_display)

        self.setLayout(layout)


class QTextEditLogger(logging.Handler):
    """
    Custom logging handler that routes log messages to a QTextEdit widget.

    Formats and displays logging messages in a Qt text display widget, enabling
    real-time monitoring of application events through the GUI.

    Args:
        text_widget (QTextEdit): The QTextEdit widget where logs will be displayed.
                                Must be initialized before passing to handler.

    Example:
        log_display = QTextEdit()
        log_handler = QTextEditLogger(log_display)
        Logger.addHandler(log_handler)
        Logger.setLevel(logging.INFO)
    """

    def __init__(self, text_widget) -> None:
        super().__init__()
        self.text_widget = text_widget
        self.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

    def emit(self, record) -> None:
        msg = self.format(record)
        self.text_widget.append(msg)


class ZmaxControlGUI(QMainWindow):
    """
    Main application window implementing the Zmax control interface.
    Manages multiple pages and coordinates communication between UI and server.
    """

    def __init__(self) -> None:
        """Initialize main window, setup UI components and data thread."""
        super().__init__()
        self.setWindowTitle(
            """SLUMBER - Sleep Logging and Unsupervised
            Monitoring through BioElectrical Recordings"""
        )
        self.setGeometry(
            settings["ui"]["window"]["window_position"][0],
            settings["ui"]["window"]["window_position"][1],
            settings["ui"]["window"]["window_size"][0],
            settings["ui"]["window"]["window_size"][1],
        )

        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create stacked widget for multiple pages
        self.stacked_widget = QStackedWidget()
        self.connection_page = ConnectionPage()
        self.control_page = ControlPage()

        self.stacked_widget.addWidget(self.connection_page)
        self.stacked_widget.addWidget(self.control_page)

        self.layout.addWidget(self.stacked_widget)

        self.signal_quality_good = False
        # Initially disable the recording buttons
        self.control_page.toggle_record_btn.setEnabled(False)

        # Set up logging to QTextEdit
        log_handler = QTextEditLogger(self.control_page.log_display)
        Logger.addHandler(log_handler)
        Logger.setLevel(settings["ui"]["console"]["log_level"])

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Initialize data thread
        self.data_thread = ZmaxDataThread()

        self._connect_signals()

    def _connect_signals(self) -> None:
        """
        Connect all UI signals to their respective slots.
        Links button clicks and thread communication signals to handler methods.
        """

        # Connect button signals
        self.connection_page.connect_btn.clicked.connect(self._handle_connect)
        self.control_page.toggle_record_btn.clicked.connect(self._toggle_recording)
        self.control_page.clear_btn.clicked.connect(self._clear_data)
        self.control_page.buffer_record_btn.clicked.connect(
            self._start_buffer_recording
        )

        # Connect thread signals
        self.data_thread.data_received.connect(self._update_status_bar)
        self.data_thread.connection_status.connect(self._handle_connection_status)
        self.data_thread.buffer_complete.connect(self._process_buffer)

    def _handle_connect(self) -> None:
        """
        Initialize server connection using user-provided host and port.
        Starts the data communication thread.
        """

        host = self.connection_page.host_input.text()
        port = int(self.connection_page.port_input.text())

        # Pass connection details to the thread before starting it
        self.data_thread.host = host
        self.data_thread.port = port
        self.data_thread.start()

    def _toggle_recording(self) -> None:
        """
        Toggle the recording state and update UI elements.
        Updates button text and logs recording status changes.
        """

        if self.data_thread.is_recording:
            # Stop recording
            self.data_thread.is_recording = False
            self.control_page.toggle_record_btn.setText("Start Recording")
            Logger.info("Recording stopped")
        else:
            # Start recording
            self.data_thread.is_recording = True
            self.control_page.toggle_record_btn.setText("Stop Recording")
            Logger.info("Recording started")

    def _clear_data(self) -> None:
        """Clear all text from the log display widget."""

        self.control_page.log_display.clear()

    def _update_status_bar(self, data: str) -> None:
        """
        Update status bar with latest data information.

        Args:
            data (str): Latest data string to display
        """

        self.status_bar.showMessage(f"Latest data: {data}")

    def _handle_connection_status(self, connected: bool) -> None:
        """
        Handle connection status changes and update UI accordingly.

        Args:
            connected (bool): True if connected, False otherwise
        """

        if connected:
            Logger.info("Connected to server")
            self.stacked_widget.setCurrentWidget(self.control_page)
        else:
            Logger.info("Connection failed")

    def _start_buffer_recording(self) -> None:
        """
        Initialize buffer recording mode.
        Disables buffer recording button until completion.
        """

        self.data_thread.is_buffer_recording = True
        Logger.info("Buffer recording started")
        self.control_page.buffer_record_btn.setEnabled(False)

    def _process_buffer(self, buffer_data: list[list[float]]) -> None:
        """
        Process completed buffer recording and evaluate signal quality.

        Args:
            buffer_data: List of recorded data points to analyze

        Effects:
            - Enables/disables recording based on signal quality
            - Updates UI elements and logs results
        """

        Logger.info("Buffer recording complete")
        self.control_page.buffer_record_btn.setEnabled(True)
        # TODO: make this more flexible, do not assume left/right
        # channel indices are columns 0 and 1

        if evaluate_signal_quality(
            np.array(buffer_data),
            sampling_rate=settings["processing"]["sample_rate"],
            duration=settings["processing"]["signal_quality_check"]["window_duration"],
        ):
            self.signal_quality_good = True
            self.control_page.toggle_record_btn.setEnabled(True)
            Logger.info("Signal quality good - Recording enabled")
        else:
            self.signal_quality_good = False
            self.control_page.toggle_record_btn.setEnabled(False)
            Logger.info("Signal quality bad - Recording not enabled")

        # Clear the buffer data after processing
        self.data_thread.buffer_data = []

    def closeEvent(self, event) -> None:
        """
        Handle application shutdown.
        Performs cleanup of connections and threads.

        Args:
            event: Close event to handle
        """

        # Stop recording if active
        if self.data_thread.is_recording:
            self._toggle_recording()

        # Signal thread to stop
        self.data_thread.is_running = False

        # Wait for thread with timeout
        if self.data_thread.isRunning():
            self.data_thread.wait(
                settings["ui"]["data_thread_timeout"] * 1000
            )  # timeout converted to ms
            if self.data_thread.isRunning():
                self.data_thread.terminate()

        # Clean up the QApplication
        QApplication.processEvents()

        event.accept()


# Entry point for standalone execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZmaxControlGUI()
    window.show()
    sys.exit(app.exec())
