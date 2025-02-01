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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, procedure: "Procedure"):
        super().__init__()
        self.setupUi(self)  # Setup the UI from the generated class

        # Home page
        self.home_page = HomePage(self)
        self.home_page.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.body_stacked_widget.addWidget(self.home_page)
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.home_page.start_signal.connect(self._start_procedure)

        # Help page
        self.help_page = HelpPage(self)
        self.help_page.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.stacked_widget.addWidget(self.help_page)
        self.help_button.clicked.connect(self._on_help_button_clicked)
        self.help_page.back_signal.connect(self._open_main_page)

        # Procedure page
        self.procedure_page = ProcedurePage(procedure, self)
        self.procedure_page.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.body_stacked_widget.addWidget(self.procedure_page)
        self.procedure_page.procedure_completed_signal.connect(
            self._on_procedure_completed
        )

    def _on_help_button_clicked(self):
        logger.info("Help button clicked")
        self.stacked_widget.setCurrentWidget(self.help_page)

    def _on_settings_button_clicked(self):
        logger.info("Settings button clicked")
        # self.stackedWidgetPages.setCurrentWidget(self.settings_page)

    def _disable_buttons(self):
        self.help_button.setEnabled(False)
        self.settings_button.setEnabled(False)

    def _enable_buttons(self):
        self.help_button.setEnabled(True)
        self.settings_button.setEnabled(True)

    def _open_main_page(self):
        logger.info("Main page opened")
        self.stacked_widget.setCurrentWidget(self.main_page)

    def _start_procedure(self):
        logger.info("Procedure started")
        self.body_stacked_widget.setCurrentWidget(self.procedure_page)

    def _on_procedure_completed(self):
        logger.info("Procedure completed")
