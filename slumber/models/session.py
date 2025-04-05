from datetime import date, datetime
from enum import Enum

from sqlalchemy import TIMESTAMP
from sqlmodel import Field, Relationship

from slumber.models.base import BaseTable
from slumber.models.condition import Condition
from slumber.models.user import User


class SessionState(Enum):
    NOT_YET_STARTED = "not yet started"
    IN_PROGRESS = "in progress"
    ENDED_NOT_COMPLETED = "ended but not completed"
    COMPLETED = "completed"


class Session(BaseTable, table=True):
    __tablename__ = "session"

    user_id: int = Field(foreign_key="user.id")
    condition_id: int = Field(foreign_key="condition.id")
    schedule_date: date
    state: SessionState = Field(default=SessionState.NOT_YET_STARTED)
    start_time: datetime | None = Field(default=None, sa_type=TIMESTAMP(timezone=True))
    end_time: datetime | None = Field(default=None, sa_type=TIMESTAMP(timezone=True))

    user: User = Relationship(back_populates="sessions")
    condition: Condition = Relationship(back_populates="sessions")
