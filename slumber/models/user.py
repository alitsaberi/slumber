import os

from sqlmodel import Session as SQLModelSession
from sqlmodel import select

from slumber.models.base import BaseTable
from slumber.utils.database import engine


class User(BaseTable, table=True):
    __tablename__ = "user"


def get_user(user_id: int | None = None) -> User:
    user_id = user_id or os.getenv("USER_ID")

    if user_id is None:
        raise ValueError("No user ID provided")

    with SQLModelSession(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if user is None:
            raise ValueError(f"User with ID {user_id} not found")
        return user
