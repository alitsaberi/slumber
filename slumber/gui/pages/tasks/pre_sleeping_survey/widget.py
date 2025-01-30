# widget.py
import json
import os
from json import JSONDecodeError
from pathlib import Path

from PySide6.QtCore import QObject, QUrl, Signal, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import QDialog, QWidget

from .help_ui import Ui_HelpDialog
from .widget_ui import Ui_Widget


class ChannelObject(QObject):
    form_complete_signal = Signal()
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

    @Slot(str)
    def saveSurveyData(self, survey_data: str) -> None:
        """
        Receive survey data from JavaScript and prints it as JSON.

        Args:
            survey_data (str): JSON string containing survey responses

        Raises:
            JSONDecodeError: If the survey data cannot be decoded as JSON
        """
        try:
            # Attempt to parse the survey data
            data = json.loads(survey_data)
        except JSONDecodeError as json_error:
            print(f"Failed to decode survey data JSON: {json_error}")
            return

        # Print the survey data as JSON
        print(json.dumps(data, indent=4))

        # Notify WidgetPage that the survey is complete
        self.form_complete_signal.emit()

    @Slot(str)
    def logError(self, error_message: str) -> None:
        """
        Handle error messages from JavaScript.

        Args:
            error_message: Error message from JavaScript
        """
        print(f"Survey GUI Error: {error_message}")


class WidgetPage(QWidget, Ui_Widget):
    is_done_signal = Signal(int)

    def __init__(self, index, status=1, parent=None):
        super().__init__(parent)
        self.index = index
        self.status = status
        self.setupUi(self)

        self.button_info.clicked.connect(self.open_help_dialog)

        self._survey_path = Path(
            os.path.join(os.path.dirname(__file__), "assets/surveys/survey.json")
        )
        html_dir = os.path.dirname(__file__)
        html_path = QUrl.fromLocalFile(os.path.join(html_dir, "assets/html/index.html"))
        self.webEngineView_pre_survey.setUrl(html_path)

        # Set up WebChannel
        self.channel = QWebChannel()
        self.channel_object = ChannelObject()
        self.channel.registerObject("channelObject", self.channel_object)
        self.webEngineView_pre_survey.page().setWebChannel(self.channel)

        self._load_survey()
        self.channel_object.form_complete_signal.connect(self.emit_done_signal)

    def _load_survey(self) -> None:
        """Load the survey HTML file and pass the full survey path as a parameter."""
        if not Path(self._survey_path).exists():
            print(f"Survey file not found: {self._survey_path}")
            return

        survey_html_path = Path(
            os.path.join(os.path.dirname(__file__), "assets/html/index.html")
        )
        file_url = QUrl.fromLocalFile(str(survey_html_path))
        file_url.setQuery(f"survey_path={self._survey_path}")
        self.webEngineView_pre_survey.setUrl(file_url)

    def emit_done_signal(self):
        print(f"Survey for task {self.index} is complete.")
        self.is_done_signal.emit(self.index)

    def start(self):
        if self.status == 1:
            print("Task started")
        else:
            print("Task already done")

    def open_help_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Help")

        ui = Ui_HelpDialog()
        ui.setupUi(dialog)

        ui.button_ok.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=True)
        )
        ui.button_cancel.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=False)
        )

        dialog.exec()

    def handle_help_response(self, dialog, accepted):
        if accepted:
            print("Help accepted.")
        else:
            print("Help canceled.")
        dialog.close()
