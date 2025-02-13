import json
from pathlib import Path

from loguru import logger
from PySide6.QtCore import QObject, QUrl, Signal, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
)
from PySide6.QtWidgets import QWidget

from slumber import settings
from slumber.gui.widgets.tasks.base import TaskPage
from slumber.utils.time import create_timestamped_name

from .widget_ui import Ui_SurveyPage

ENCODING = "utf-8"
HTML_FILE_PATH = Path(__file__).parent / "assets" / "index.html"
SURVEY_RESPONSE_EXTENSION = "json"


class ChannelObject(QObject):
    survey_complete = Signal(str)
    """Handle JavaScript-Python communication via QWebChannel.

    This class provides methods that can be accessed from JavaScript to
    save survey data and log error messages to the Python backend.
    """

    @Slot(str)
    def handle_survey_submission(self, survey_data: str) -> None:
        """
        Validate and emit survey data received from JavaScript.

        Args:
            survey_data (str): JSON string containing survey responses
        """
        try:
            _ = json.loads(survey_data)  # Validate JSON format
            self.survey_complete.emit(survey_data)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid survey data received: {e}")

    @Slot(str)
    def handle_log(self, message: str) -> None:
        """
        Handle console log messages from JavaScript frontend.
        """
        logger.debug(f"JS console log: {message}")

    @Slot(str)
    def handle_error(self, error_message: str) -> None:
        """
        Handle error messages from JavaScript frontend.
        """
        logger.error(f"JS error: {error_message}")


class SurveyWebPage(QWebEnginePage):
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.featurePermissionRequested.connect(self._handle_permission_request)

    def _handle_permission_request(
        self, url: QUrl, feature: QWebEnginePage.Feature
    ) -> None:
        if feature in (QWebEnginePage.Feature.MediaAudioCapture,):
            self.setFeaturePermission(
                url, feature, QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )
        else:
            self.setFeaturePermission(
                url, feature, QWebEnginePage.PermissionPolicy.PermissionDeniedByUser
            )


class SurveyPage(TaskPage, Ui_SurveyPage):
    def __init__(
        self,
        index: int,
        title: str,
        survey_config_path: Path | str,
        output_directory: Path | str,
        parent: QWidget | None = None,
    ):
        super().__init__(index, title, parent=parent)

        self.survey_config_path = Path(survey_config_path).absolute()
        if not self.survey_config_path.exists():
            raise FileNotFoundError(f"Survey file not found: {self.survey_config_path}")

        self.output_directory = Path(output_directory)

        self.web_engine_view.setPage(SurveyWebPage(self.web_engine_view))

        self._init_web_channel()
        self._load_survey()
        self._connect_signals()

    def _init_web_channel(self) -> None:
        """Initialize and set up the WebChannel for JavaScript-Python communication."""
        self.channel = QWebChannel()
        self.channel_object = ChannelObject()
        self.channel.registerObject("channelObject", self.channel_object)
        self.web_engine_view.page().setWebChannel(self.channel)

    def _connect_signals(self) -> None:
        self.channel_object.survey_complete.connect(self.done)

    def _load_survey(self) -> None:
        """Load the survey HTML file and pass the full survey path as a parameter."""

        if not HTML_FILE_PATH.exists():
            raise FileNotFoundError(f"HTML template not found: {HTML_FILE_PATH}")

        html_url = QUrl.fromLocalFile(HTML_FILE_PATH)
        html_url.setQuery(f"survey_path={self.survey_config_path}")

        logger.debug(f"Loading survey from {html_url}")
        self.web_engine_view.setUrl(html_url)

    def done(self, survey_data: str) -> None:
        if self.output_directory is not None:
            self._save_survey_data(survey_data)

        super().done()

    def _save_survey_data(self, survey_data: str) -> None:
        self.output_directory.mkdir(parents=True, exist_ok=True)
        survey_data_path = self.output_directory / create_timestamped_name(
            self.survey_config_path.stem, "json"
        )
        with open(survey_data_path, "w") as f:
            json.dump(
                json.loads(survey_data), f, indent=settings["survey"]["response_indent"]
            )
        logger.info(f"Survey data saved to {survey_data_path}")
