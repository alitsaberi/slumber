# FILE: home.py

from pathlib import Path

from loguru import logger
from PySide6.QtCore import QUrl, Signal
from PySide6.QtWidgets import QWidget

from .widget_ui import Ui_HomePage

HTML_FILE_PATH = Path(__file__).parent / "assets" / "html" / "index.html"


class HomePage(QWidget, Ui_HomePage):
    start_signal = Signal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.web_engine_view.setUrl(QUrl.fromLocalFile(HTML_FILE_PATH))
        self.start_button.clicked.connect(self.on_start_button_clicked)

    def on_start_button_clicked(self):
        logger.info("Start button clicked")
        self.start_signal.emit()
