from typing import TYPE_CHECKING

from sqlmodel import Relationship

from slumber.models.base import BaseTable

if TYPE_CHECKING:
    from slumber.models.session import Session


class User(BaseTable, table=True):
    __tablename__ = "user"

    sessions: list["Session"] = Relationship(back_populates="user")
