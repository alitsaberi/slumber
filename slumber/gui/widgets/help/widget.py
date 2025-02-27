from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from pydantic import (
    BaseModel,
    FilePath,
    TypeAdapter,
    computed_field,
)
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from slumber.utils.helpers import load_yaml

from .widget_ui import Ui_HelpPage

ASSETS_DIR = Path(__file__).parent / "assets"
HTML_FILE_NAME = "index.html"
CSS_FILE_PATH = ASSETS_DIR / "css" / "style.css"


class Item(BaseModel):
    question: str
    instruction_path: FilePath

    @computed_field
    @property
    def markdown_content(self) -> str:
        return self.instruction_path.read_text(encoding="utf-8")

    @computed_field
    @property
    def html_content(self) -> str:
        return markdown.markdown(
            self.markdown_content,
            extensions=["extra", "nl2br", "sane_lists"],
            output_format="html5",
        )


class HelpPage(QWidget, Ui_HelpPage):
    back_signal = Signal()

    def __init__(self, config_path: Path, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)

        self.config = TypeAdapter(list[Item]).validate_python(load_yaml(config_path))

        self._generate_html()
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.back_button.clicked.connect(self.on_back_button_clicked)

    def on_back_button_clicked(self):
        logger.info("Back button clicked")
        self.back_signal.emit()

    def _generate_html(self) -> None:
        env = Environment(loader=FileSystemLoader(ASSETS_DIR))
        template = env.get_template(HTML_FILE_NAME)
        css_content = CSS_FILE_PATH.read_text(encoding="utf-8")
        rendered_html = template.render(faq_items=self.config, css=css_content)
        logger.debug(f"Rendered HTML: {rendered_html}")
        self.web_engine_view.setHtml(rendered_html)
