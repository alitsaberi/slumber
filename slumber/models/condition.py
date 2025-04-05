from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Relationship

from slumber.models.base import BaseTable
from slumber.models.dag import CollectionConfig
from slumber.models.gui import GUIConfig

if TYPE_CHECKING:
    from slumber.models.session import Session


class ConditionConfig(BaseModel):
    name: str
    gui: GUIConfig
    dag: CollectionConfig


class Condition(BaseTable, table=True):
    __tablename__ = "condition"

    name: str

    sessions: list["Session"] = Relationship(back_populates="condition")
