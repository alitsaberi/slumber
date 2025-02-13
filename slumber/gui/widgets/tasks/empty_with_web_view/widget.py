from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QWidget

from slumber.gui.widgets.tasks.base import TaskPage

from .widget_ui import Ui_EmptyWebPage

HTML_FILE_PATH = Path(__file__).parent / "assets" / "index.html"


class EmptyWebPage(TaskPage, Ui_EmptyWebPage):
    def __init__(self, index: int, title: str, parent: QWidget = None):
        super().__init__(index, title, parent=parent)

        self._connect_signals()

        html_url = QUrl.fromLocalFile(HTML_FILE_PATH)
        self.web_engine_view.setUrl(html_url)

    def _connect_signals(self) -> None:
        self.done_button.clicked.connect(self.done)
