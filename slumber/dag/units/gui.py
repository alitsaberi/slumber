from importlib import import_module
import inspect
from types import ModuleType
from typing import Annotated, Any

import ezmsg.core as ez
from loguru import logger
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator
from PySide6.QtWidgets import QApplication

from slumber import settings
from slumber.dag.utils import PydanticSettings
from slumber.gui.main_window import MainWindow
from slumber.gui.widgets import tasks
from slumber.gui.widgets.tasks.base.widget import TaskPage
from slumber.scripts.create_task import TASKS_DIR_NAME
from slumber.utils.helpers import create_class_by_name_resolver

DEFAULTS = settings["gui"]


class Task(BaseModel):
    title: str = Field(min_length=1)
    widget: type[TaskPage]

    model_config = ConfigDict(strict=False, arbitrary_types_allowed=True)

    @field_validator("widget", mode="before")
    def validate_widget(cls, v: Any) -> Any:
        if isinstance(v, str):
            try:
                module = getattr(tasks, v)
            except AttributeError as e:
                raise ValueError(f"Could not find a module named {v} in {tasks}") from e

            for _, obj in inspect.getmembers(module.widget, inspect.isclass):
                if issubclass(obj, TaskPage):
                    return obj

            raise ValueError(f"Could not find a TaskPage widget in {v}")

        return v


class Procedure(BaseModel):
    name: str
    tasks: list[Task] = Field(min_length=1)

    @property
    def n_tasks(self) -> int:
        return len(self.tasks)


class Settings(PydanticSettings):
    procedures: list[Procedure] = Field(min_length=1)


class State(ez.State):
    app: QApplication
    window: MainWindow


class GUI(ez.Unit):
    SETTINGS = Settings
    STATE = State

    def initialize(self) -> None:
        self.STATE.app = QApplication()
        self.STATE.window = MainWindow(procedure=self.SETTINGS.procedures[0])
        self.STATE.window.show()

    def shutdown(self):
        self.STATE.window.close()
        self.STATE.app.quit()

    @ez.task
    async def run(self) -> None:
        self.STATE.app.exec()
        raise ez.NormalTermination
