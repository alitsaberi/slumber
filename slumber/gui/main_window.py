import typing
from multiprocessing import Pipe, Process
from multiprocessing.connection import PipeConnection

from loguru import logger
from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QMainWindow,
    QSizePolicy,
)

from slumber import settings
from slumber.dag.units.home_lucid_dreaming.master import ExperimentState
from slumber.gui.widgets.help.widget import HelpPage
from slumber.gui.widgets.home.widget import HomePage
from slumber.gui.widgets.procedure.widget import ProcedurePage
from slumber.gui.widgets.sleep.widget import SleepPage, State
from slumber.models.condition import Condition
from slumber.models.dag import CollectionConfig
from slumber.models.gui import Procedure

from .main_window_ui import Ui_MainWindow

EXPANDING_POLICY = QSizePolicy.Policy.Expanding
DEFAULT_WIDGET_POLICY = (EXPANDING_POLICY, EXPANDING_POLICY)


class MainWindow(QMainWindow, Ui_MainWindow):
    experiment_state = Signal(ExperimentState)
    audio_cue_calibrated = Signal(int)
    light_cue_calibrated = Signal(int)

    def __init__(
        self,
        condition: Condition,
        run_dag_function: typing.Callable[[CollectionConfig], None],
    ):
        super().__init__()
        self.setupUi(self)  # Setup the UI from the generated class

        self.dag = condition.dag
        self.run_dag_function = run_dag_function
        self.help_page_config_path = condition.gui.help_page_config_path
        self.pre_sleep_procedure = condition.gui.pre_sleep_procedure
        self.awakening_procedure = condition.gui.awakening_procedure
        self.post_sleep_procedure = condition.gui.post_sleep_procedure
        self.wbtb_procedure = condition.gui.wbtb_procedure

        self._initialize_widgets()
        self.set_procedure(self.pre_sleep_procedure, self._on_pre_sleep_procedure_done)
        self.state: State | None = None
        self.dag_process: Process | None = None
        self.dag_connection: PipeConnection | None = None

        self.settings_button.setVisible(False)

        self.audio_cue_calibrated.connect(self._set_minimum_subjective_audio_intensity)
        self.light_cue_calibrated.connect(self._set_minimum_subjective_light_intensity)

    def closeEvent(self, event: QCloseEvent) -> None:
        self._terminate_dag_process()
        super().closeEvent(event)

    def _initialize_widgets(self) -> None:
        self._setup_home_page()
        self._setup_help_page()
        self._setup_procedure_page()
        self._setup_sleep_page()

    def _setup_home_page(self) -> None:
        self.home_page = HomePage(self)
        self.home_page.setSizePolicy(*DEFAULT_WIDGET_POLICY)
        self.body_stacked_widget.addWidget(self.home_page)
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.home_page.start_signal.connect(self.start_procedure)

    def _setup_help_page(self) -> None:
        self.help_page = HelpPage(self.help_page_config_path, self)
        self.help_page.setSizePolicy(*DEFAULT_WIDGET_POLICY)
        self.stacked_widget.addWidget(self.help_page)
        self.help_button.clicked.connect(self._on_help_button_clicked)
        self.help_page.back_signal.connect(self._open_main_page)

    def _setup_procedure_page(self) -> None:
        self.procedure_page = ProcedurePage(self)
        self.procedure_page.setSizePolicy(*DEFAULT_WIDGET_POLICY)
        self.body_stacked_widget.addWidget(self.procedure_page)

    def _setup_sleep_page(self) -> None:
        self.sleep_page = SleepPage(self)
        self.sleep_page.setSizePolicy(*DEFAULT_WIDGET_POLICY)
        self.body_stacked_widget.addWidget(self.sleep_page)
        self.sleep_page.state_changed.connect(self._on_sleep_state_changed)
        self.sleep_page.end_session.connect(self._end_session)

    def _on_help_button_clicked(self) -> None:
        logger.info("Help button clicked")
        self.stacked_widget.setCurrentWidget(self.help_page)

    def _on_settings_button_clicked(self) -> None:
        logger.info("Settings button clicked")

    def _open_main_page(self) -> None:
        logger.info("Main page opened")
        self.stacked_widget.setCurrentWidget(self.main_page)

    def _on_pre_sleep_procedure_done(self) -> None:
        logger.info("Pre-sleep procedure done")
        self.dag_process, self.dag_connection = self._setup_dag_process()
        self._open_sleep_page()

    def _open_sleep_page(self) -> None:
        logger.info("Sleep page opened")
        self.body_stacked_widget.setCurrentWidget(self.sleep_page)
        self.set_procedure(self.awakening_procedure, self._open_sleep_page)

    def _on_sleep_state_changed(self, state: State) -> None:
        logger.info(f"Sleep state changed to {state}")

        if self.state is None:
            logger.info("Starting the DAG process")
            self.dag_process.start()

        self.state = state

        if state == State.Awake:
            self.start_procedure()
            self.dag_connection.send(ExperimentState.AWAKE)
        else:
            self.dag_connection.send(ExperimentState.ASLEEP)

    def _setup_dag_process(self) -> tuple[Process, PipeConnection]:
        parent_connection, child_connection = Pipe()
        self.dag.components_mapping["MASTER"].settings["gui_connection"] = (
            child_connection
        )
        logger.info(f"Creating the DAG process: {self.dag}")
        process = Process(
            target=self.run_dag_function,
            args=(self.dag,),
            name="dag_process",
        )
        return process, parent_connection

    def start_procedure(self) -> None:
        logger.info("Procedure started")
        self.body_stacked_widget.setCurrentWidget(self.procedure_page)

    def set_procedure(
        self, procedure: "Procedure", callback: typing.Callable = None
    ) -> None:
        logger.info(f"Setting procedure: {procedure}")
        self.procedure_page.done_signal.disconnect()
        self.procedure_page.set_procedure(procedure)
        if callback:
            self.procedure_page.done_signal.connect(callback)

    def _set_minimum_subjective_audio_intensity(self, value: int) -> None:
        logger.info(f"Setting minimum subjective audio intensity to {value}")
        self.dag.components_mapping["REM_CUEING"].settings["auditory_cueing"][
            "intensity"
        ]["value"] = value
        # TODO: not the best way to do this

    def _set_minimum_subjective_light_intensity(self, value: int) -> None:
        logger.info(f"Setting minimum subjective light intensity to {value}")
        self.dag.components_mapping["REM_CUEING"].settings["visual_cueing"][
            "intensity"
        ]["value"] = value
        # TODO: not the best way to do this

    def _end_session(self) -> None:
        logger.info("Ending session")
        self.set_procedure(self.post_sleep_procedure, self.close)
        self._terminate_dag_process()
        self.start_procedure()

    def _terminate_dag_process(self) -> None:
        if self.dag_process is not None and self.dag_process.is_alive():
            logger.info("Terminating DAG process")
            self.dag_process.terminate()
            self.dag_process.join(settings["process_termination_timeout"])
