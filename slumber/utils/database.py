import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    from slumber.models.condition import Condition  # noqa: F401
    from slumber.models.session import Session  # noqa: F401
    from slumber.models.user import User  # noqa: F401

    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
