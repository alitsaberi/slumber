from pydantic import BaseModel

from slumber.models.dag import CollectionConfig
from slumber.models.gui import GUIConfig


class Condition(BaseModel):
    name: str
    gui: GUIConfig
    dag: CollectionConfig
