from datetime import datetime

from sqlalchemy import TIMESTAMP, func, text
from sqlmodel import Field, SQLModel


class BaseTable(SQLModel):
    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")},
        nullable=False,
    )

    updated_at: datetime | None = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"onupdate": func.now(), "nullable": True},
    )
