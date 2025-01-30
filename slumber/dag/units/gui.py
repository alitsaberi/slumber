from dataclasses import asdict
from importlib import import_module
from types import ModuleType
from typing import Any
import ezmsg.core as ez
from loguru import logger
from pydantic import BaseModel, Field, field_validator
from PySide6.QtWidgets import QApplication

from slumber.dag.utils import PydanticSettings
from slumber.gui.main_window import MainWindow
from slumber.models.gui_config_model import get_gui_config
from slumber.models.study_config_model import get_study_config
from slumber.models.tasks_model import get_tasks
from slumber.scripts.create_task import TASKS_DIR_NAME
from slumber import settings
    
    
DEFAULTS = settings["gui"]
    
class Task(BaseModel):
    title: str = Field(min_length=1)
    module: ModuleType

    @field_validator("module", mode="before")
    @classmethod
    def validate_tasks(cls, module: Any) -> list[ModuleType]:
        if isinstance(module, str):
            module = import_module(f".{TASKS_DIR_NAME}.module")
        return module

    
class Procedure(BaseModel):
    name: str
    tasks: list[Task]


class Settings(PydanticSettings):
    procedures = list[Procedure]


class State(ez.State):
    app: QApplication
    window: MainWindow


class GUI(ez.Unit):
    SETTINGS = Settings
    STATE = State

    def initialize(self) -> None:
        self.STATE.app = QApplication()
        self.STATE.window = MainWindow(**asdict(self.SETTINGS))
        self.STATE.window.show()

    def shutdown(self):
        self.STATE.window.close()
        self.STATE.app.quit()

    @ez.task
    async def run(self) -> None:
        self.STATE.app.exec()
        raise ez.NormalTermination
