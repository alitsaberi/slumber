import ezmsg.core as ez
from loguru import logger
from pydantic import BaseModel
from PySide6.QtWidgets import QApplication

from slumber.dag.utils import PydanticSettings
from slumber.gui.main_window import MainWindow
from slumber.models.gui_config_model import get_gui_config
from slumber.models.study_config_model import get_study_config
from slumber.models.tasks_model import get_tasks


class Task(BaseModel):
    name: str
    header: str
    module: str
    type: str
    enabled: bool


class Settings(PydanticSettings):
    tasks: list[Task]


class State(ez.State):
    app: QApplication
    window: MainWindow


class GUI(ez.Unit):
    SETTINGS = Settings
    STATE = State

    def initialize(self) -> None:
        self.STATE.app = QApplication()

        gui_config = get_gui_config()
        study_config = get_study_config()
        tasks = get_tasks()
        logger.error(tasks)
        self.STATE.window = MainWindow(gui_config, study_config, tasks)
        self.STATE.window.show()

    def shutdown(self):
        self.STATE.window.close()
        self.STATE.app.quit()

    @ez.task
    async def run(self) -> None:
        self.STATE.app.exec()
        raise ez.NormalTermination
