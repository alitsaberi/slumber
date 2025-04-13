from datetime import datetime

from sqlalchemy import TIMESTAMP, func, text
from sqlmodel import Field, SQLModel

from slumber.utils.time import now


class BaseTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        default_factory=now,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
    )

    updated_at: datetime = Field(
        default_factory=now,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "onupdate": func.now(),
        },
    )
