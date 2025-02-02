from pathlib import Path

from loguru import logger
from PySide6.QtCore import QUrl, Signal
from PySide6.QtWidgets import QWidget

from .widget_ui import Ui_HelpPage

HTML_FILE_PATH = Path(__file__).parent / "assets" / "html" / "index.html"


class HelpPage(QWidget, Ui_HelpPage):
    back_signal = Signal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)  # Setup the UI from the generated class

        self.back_button.clicked.connect(self.on_back_button_clicked)
        self.web_engine_view.setUrl(QUrl.fromLocalFile(HTML_FILE_PATH))

    def on_back_button_clicked(self):
        logger.info("Back button clicked")
        self.back_signal.emit()
