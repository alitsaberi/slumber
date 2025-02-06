import importlib
import inspect
from typing import Any

import ezmsg.core as ez
from pydantic import BaseModel, ConfigDict, Field, field_validator
from PySide6.QtWidgets import QApplication

from slumber import settings
from slumber.dag.utils import PydanticSettings
from slumber.gui.main_window import MainWindow
from slumber.gui.widgets import tasks
from slumber.gui.widgets.tasks.base import TaskPage

DEFAULTS = settings["gui"]


class Task(BaseModel):
    title: str = Field(min_length=1)
    widget: type[TaskPage]
    kwargs: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(strict=False, arbitrary_types_allowed=True)

    @field_validator("widget", mode="before")
    def validate_widget(cls, v: Any) -> Any:
        if isinstance(v, str):
            try:
                widget_module = importlib.import_module(f"{tasks.__name__}.{v}.widget")
            except ModuleNotFoundError as e:
                raise ValueError(f"{e}") from e

            for _, obj in inspect.getmembers(widget_module, inspect.isclass):
                if issubclass(obj, TaskPage) and obj != TaskPage:
                    return obj

            raise ValueError(f"Could not find a {TaskPage.__name__} widget in {v}")

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
        self.STATE.window = MainWindow(procedures=self.SETTINGS.procedures)
        self.STATE.window.show()

    def shutdown(self):
        self.STATE.window.close()
        self.STATE.app.quit()

    @ez.task
    def run(self) -> None:
        self.STATE.app.exec()
        raise ez.NormalTermination
