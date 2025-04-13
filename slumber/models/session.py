import os
from collections.abc import Callable
from datetime import date, datetime
from functools import partial
from pathlib import Path

import ezmsg.core as ez
from loguru import logger
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import selectinload
from sqlmodel import Field, Relationship, select
from sqlmodel import Session as SQLModelSession

from slumber import SESSIONS_DIR, settings
from slumber.models.base import BaseTable
from slumber.models.condition import Condition, get_condition_by_id
from slumber.models.dag import CollectionConfig
from slumber.models.user import User
from slumber.sources.zmax import open_quick_start
from slumber.utils.database import engine
from slumber.utils.logger import add_file_handler
from slumber.utils.time import create_timestamped_name

LOGS_DIR_NAME = "logs"
DATA_DIR_NAME = "data"
RUN_DIR_SUBDIRECTORIES = [LOGS_DIR_NAME, DATA_DIR_NAME]


class Session(BaseTable, table=True):
    __tablename__ = "session"

    user_id: int = Field(foreign_key="user.id")
    condition_id: int = Field(foreign_key="condition.id")
    scheduled_date: date
    start_time: datetime | None = Field(default=None, sa_type=TIMESTAMP(timezone=True))
    end_time: datetime | None = Field(default=None, sa_type=TIMESTAMP(timezone=True))

    user: User = Relationship()
    condition: Condition = Relationship()


def get_scheduled_session(scheduled_date: date, user_id: int | None = None) -> Session:
    user_id = user_id or os.getenv("USER_ID")

    if user_id is None:
        raise ValueError("No user ID provided")

    with SQLModelSession(engine) as session:
        scheduled_session = session.exec(
            select(Session)
            .options(selectinload(Session.user), selectinload(Session.condition))
            .where(
                Session.user_id == user_id,
                Session.scheduled_date == scheduled_date,
            )
        ).one()

        return scheduled_session


def update_session_state(
    session_obj: Session,
    start_time: datetime = None,
    end_time: datetime = None,
) -> None:
    """
    Update the state of a session in the database.

    Args:
        session_obj: The session object to update
        start_time: Session start time (optional)
        end_time: Session end time (optional)
    """

    if start_time is not None:
        session_obj.start_time = start_time

    if end_time is not None:
        session_obj.end_time = end_time

    with SQLModelSession(engine) as session:
        session.add(session_obj)
        session.commit()
        session.refresh(session_obj)


def _create_run_subdirectories(run_directory: Path) -> None:
    for subdirectory_name in RUN_DIR_SUBDIRECTORIES:
        subdirectory = run_directory / subdirectory_name
        subdirectory.mkdir()
        logger.info(f"Created {subdirectory_name} directory: {subdirectory}")


def _create_run_directory(condition_name: str) -> Path:
    if not SESSIONS_DIR.exists():
        logger.info(f"Sessions directory does not exist. Creating {SESSIONS_DIR}...")
        SESSIONS_DIR.mkdir()

    directory = SESSIONS_DIR / create_timestamped_name(condition_name)

    if directory.exists():
        raise FileExistsError(f"Session directory {directory} already exists.")

    directory.mkdir()
    logger.info(f"Created run directory: {directory}")

    _create_run_subdirectories(directory)

    return directory.absolute()


def run_dag(logs_dir: Path, dag_config: CollectionConfig) -> None:
    add_file_handler(logs_dir / settings["logging"]["dag_log_file"])
    ez.run(**dag_config.configure())


def run_session(session: Session) -> tuple[Condition, Callable]:
    condition = get_condition_by_id(session.condition_id)
    logger.info(f"Running session: {session.id} with condition: {condition.name}")

    run_directory = _create_run_directory(condition.name)

    logs_dir = run_directory / LOGS_DIR_NAME
    add_file_handler(logs_dir / "gui.log")

    os.chdir(run_directory)

    open_quick_start()

    run_dag_function = partial(run_dag, logs_dir)
    return condition, run_dag_function
