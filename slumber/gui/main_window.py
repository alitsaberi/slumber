import typing

from loguru import logger
from PySide6.QtWidgets import (
    QMainWindow,
    QSizePolicy,
)

from slumber.gui.widgets.help.widget import HelpPage
from slumber.gui.widgets.home.widget import HomePage
from slumber.gui.widgets.procedure.widget import ProcedurePage

from .main_window_ui import Ui_MainWindow

if typing.TYPE_CHECKING:
    from slumber.dag.units.gui import Procedure


EXPANDING_POLICY = QSizePolicy.Policy.Expanding
DEFAULT_WIDGET_POLICY = (EXPANDING_POLICY, EXPANDING_POLICY)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(
        self,
    ):
        super().__init__()
        self.setupUi(self)  # Setup the UI from the generated class
        self._initialize_widgets()

    def _initialize_widgets(self) -> None:
        self._setup_home_page()
        self._setup_help_page()
        self._setup_procedure_page()

    def _setup_home_page(self) -> None:
        self.home_page = HomePage(self)
        self.home_page.setSizePolicy(*DEFAULT_WIDGET_POLICY)
        self.body_stacked_widget.addWidget(self.home_page)
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.home_page.start_signal.connect(self._start_procedure)

    def _setup_help_page(self) -> None:
        self.help_page = HelpPage(self)
        self.help_page.setSizePolicy(*DEFAULT_WIDGET_POLICY)
        self.stacked_widget.addWidget(self.help_page)
        self.help_button.clicked.connect(self._on_help_button_clicked)
        self.help_page.back_signal.connect(self._open_main_page)

    def _setup_procedure_page(self) -> None:
        self.procedure_page = ProcedurePage(self)
        self.procedure_page.setSizePolicy(*DEFAULT_WIDGET_POLICY)
        self.body_stacked_widget.addWidget(self.procedure_page)

    def _on_help_button_clicked(self) -> None:
        logger.info("Help button clicked")
        self.stacked_widget.setCurrentWidget(self.help_page)

    def _on_settings_button_clicked(self) -> None:
        logger.info("Settings button clicked")

    def _open_main_page(self) -> None:
        logger.info("Main page opened")
        self.stacked_widget.setCurrentWidget(self.main_page)

    def _start_procedure(self) -> None:
        logger.info("Procedure started")
        self.body_stacked_widget.setCurrentWidget(self.procedure_page)

    def set_procedure(
        self, procedure: "Procedure", callback: typing.Callable = None
    ) -> None:
        self.procedure_page.done_signal.disconnect()
        self.procedure_page.set_procedure(procedure)
        if callback:
            self.procedure_page.done_signal.connect(callback)
