import importlib
import inspect
from multiprocessing.connection import PipeConnection
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from slumber.gui.widgets import tasks
from slumber.gui.widgets.tasks.base import TaskPage


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
    tasks: list[Task] = Field(min_length=1)

    @property
    def n_tasks(self) -> int:
        return len(self.tasks)


class GUIConfig(BaseModel):
    dag_connection: PipeConnection
    pre_sleep_procedure: Procedure = Field(alias="pre_sleep")
    awakening_procedure: Procedure = Field(alias="awakening")
    post_sleep_procedure: Procedure = Field(alias="post_sleep")
    wbtb_procedure: Procedure | None = Field(None, alias="wbtb")

    model_config = ConfigDict(arbitrary_types_allowed=True)
