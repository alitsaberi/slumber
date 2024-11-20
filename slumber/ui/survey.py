"""
Survey GUI Module

Provides a PyQt6-based GUI for displaying and handling surveys using SurveyJS.
Facilitates communication between JavaScript (frontend) and Python (backend)
via QWebChannel.

Classes:
    ChannelObject: Custom QObject for handling communication
                    between JavaScript and Python.
    SurveyWindow: Main window for displaying surveys using QWebEngineView.
"""

import json
import logging
import sys
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path

from loguru import logger
from PyQt6.QtCore import QObject, QUrl, pyqtSlot
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from slumber import settings

WINDOW_TITLE = "Questionnaires"
WINDOW_GEOMETRY = (100, 100, 1024, 768)
SURVEY_HTML_PATH = Path(__file__).parent / "assets" / "html" / "survey.html"

SURVEY_DATA_DIR = Path(__file__).parents[2] / settings["storage"]["survey_data_dir"]
DATETIME_FORMAT = settings["storage"]["datetime_format"]


class ChannelObject(QObject):
    """Handle JavaScript-Python communication via QWebChannel.

    This class provides methods that can be accessed from JavaScript to
    save survey data and log error messages to the Python backend.

    Attributes:
        None (all methods are accessed directly via QWebChannel).

    Methods:
        saveSurveyData(str): Sends survey data from JavaScript to Python for saving it
                            to a JSON file.
        logError(str): Logs error messages received from JavaScript.
    """

    # TODO: Decide how we want to save the data:
    # (where, how - multiple files or single file, which format - .json, .csv, etc.)

    @pyqtSlot(str)
    def saveSurveyData(self, survey_data: str) -> None:
        """
        Receive survey data from JavaScript and saves it to a JSON file.

        Args:
            survey_data (str): JSON string containing survey responses

        Raises:
            JSONDecodeError: If the survey data cannot be decoded as JSON
        """
        try:
            # Attempt to parse the survey data
            data = json.loads(survey_data)
        except JSONDecodeError as json_error:
            logger.error(f"Failed to decode survey data JSON: {json_error}")
            return

        try:
            # Ensure the survey data directory exists
            SURVEY_DATA_DIR.mkdir(parents=True, exist_ok=True)

            # Generate unique file name based on timestamp
            timestamp = datetime.now().strftime(DATETIME_FORMAT)
            file_path = SURVEY_DATA_DIR / f"survey_results_{timestamp}.json"

            # Save survey data to JSON file
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            logger.info(f"Survey data saved successfully to {file_path}")

        except OSError as os_error:
            # Handles file-related errors, such as permission issues,
            # missing directories, disk full, etc.
            logger.error(f"File I/O error while saving survey data: {os_error}")

    @pyqtSlot(str)
    def logError(self, error_message: str) -> None:
        """
        Handle error messages from JavaScript.

        Args:
            error_message: Error message from JavaScript
        """
        logging.error(f"Survey GUI Error: {error_message}")


class SurveyWindow(QMainWindow):
    """Main window for displaying surveys using QWebEngineView.

    This class provides a GUI window that displays surveys using a web-based
    interface. It facilitates the setup and management of QWebChannel
    communication for real-time interactions with JavaScript.

    Attributes:
        _survey_path (str): Path to the survey JSON file.
        webview (QWebEngineView): Displays the survey interface.

    Methods:
        _setup_ui(): Configures the main UI components, including the window title,
            geometry, and central widget layout.
        setup_web_channel(): Sets up QWebChannel for JavaScript-Python communication.
        _load_survey(): Loads the survey HTML file and sets the full survey path
                        as a parameter.
        closeEvent(QCloseEvent): Handles window close events and performs
                                resource cleanup.

    Example:
        window = SurveyWindow(survey_path="path/to/survey.json")
        window.show()
    """

    def __init__(
        self,
        survey_path: str,
    ) -> None:
        """
        Initialize the survey window.

        Args:
            survey_path: Path to the survey JSON file
        """
        super().__init__()
        self._survey_path = survey_path
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        # Configure window
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(*WINDOW_GEOMETRY)

        # Set up central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Initialize web view
        self.webview = QWebEngineView()
        self.setup_web_channel()
        self._load_survey()

        layout.addWidget(self.webview)

    def setup_web_channel(self) -> None:
        """Configure the web channel for JavaScript-Python communication."""
        self.channel = QWebChannel()
        self.channel_object = ChannelObject()
        self.channel.registerObject("channelObject", self.channel_object)
        self.webview.page().setWebChannel(self.channel)

    def _load_survey(self) -> None:
        """Load the survey HTML file and pass the full survey path as a parameter."""
        if not Path(self._survey_path).exists():
            logger.error(f"Survey file not found: {self._survey_path}")
            return

        survey_html_path = SURVEY_HTML_PATH
        file_url = QUrl.fromLocalFile(str(survey_html_path))
        file_url.setQuery(f"survey_path={self._survey_path}")
        self.webview.setUrl(file_url)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Handles window close event and resource cleanup.

        Args:
            event (QCloseEvent): The close event triggered when the window is
            about to close.
        """
        # Clean up resources
        self.webview.deleteLater()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the survey name
    survey_name = "sample_survey"

    # Construct the full path to the survey JSON file based on survey_name
    survey_path = (
        Path(__file__).parents[2] / "configs" / "surveys" / f"{survey_name}.json"
    )

    window = SurveyWindow(survey_path=survey_path)
    window.show()
    sys.exit(app.exec())
