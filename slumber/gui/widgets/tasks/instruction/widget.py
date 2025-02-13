from pathlib import Path

import markdown
from jinja2 import Template
from loguru import logger
from PySide6.QtWidgets import QWidget

from slumber.gui.widgets.tasks.base import TaskPage

from .widget_ui import Ui_EmptyWebPage

ASSETS_DIR = Path(__file__).parent / "assets"
HTML_FILE_PATH = ASSETS_DIR / "index.html"
CSS_FILE_PATH = ASSETS_DIR / "css" / "style.css"


class EmptyWebPage(TaskPage, Ui_EmptyWebPage):
    def __init__(
        self,
        index: int,
        title: str,
        instruction_path: Path | str,
        parent: QWidget = None,
    ):
        super().__init__(index, title, parent=parent)

        self.instruction_path = Path(instruction_path).absolute()
        if not self.instruction_path.exists():
            raise FileNotFoundError(
                f"Instruction file not found: {self.instruction_path}"
            )

        self._connect_signals()
        self._load_markdown_content()

    def _load_markdown_content(self) -> None:
        markdown_content = self.instruction_path.read_text(encoding="utf-8")
        html_content = markdown.markdown(markdown_content)
        logger.debug(f"Markdown content: {html_content}")
        css_content = CSS_FILE_PATH.read_text(encoding="utf-8")
        template = Template(HTML_FILE_PATH.read_text(encoding="utf-8"))
        rendered_html = template.render(content=html_content, css=css_content)
        logger.debug(f"Rendered HTML: {rendered_html}")
        self.web_engine_view.setHtml(rendered_html)

    def _connect_signals(self) -> None:
        self.done_button.clicked.connect(self.done)
