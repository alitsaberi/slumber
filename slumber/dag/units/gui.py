import asyncio

import ezmsg.core as ez
import qasync
from PySide6.QtWidgets import QApplication

from slumber.dag.utils import PydanticSettings
from slumber.gui.main_window import MainWindow
from slumber.main import insert_default_configs, read_yaml_config
from slumber.model.gui_config_model import get_gui_config
from slumber.model.study_config_model import get_study_config
from slumber.model.tasks_model import get_tasks
from slumber.utils.db_utils import initialize_db


class Settings(PydanticSettings):
    pass


class State(ez.State):
    app: QApplication
    window: MainWindow


class GUI(ez.Unit):
    SETTINGS = Settings
    STATE = State

    def initialize(self) -> None:
        self.STATE.app = QApplication()
        self.STATE.loop = qasync.QEventLoop(self.STATE.app)
        asyncio.set_event_loop(self.STATE.loop)
        yaml_config_path = "C:/Users/Mahdad/Projects/slumber/configs/settings.yaml"
        yaml_config = read_yaml_config(yaml_config_path)

        # Initialize the database
        initialize_db()

        # Insert default configs if not exists
        insert_default_configs(yaml_config)

        gui_config = get_gui_config()
        study_config = get_study_config()
        tasks = get_tasks()
        self.STATE.window = MainWindow(gui_config, study_config, tasks)
        self.STATE.window.show()

    def shutdown(self):
        pass

    @ez.task
    async def run(self) -> None:
        self.STATE.app.exec()
