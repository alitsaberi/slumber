from typing import Any

from loguru import logger
from sqlmodel import JSON, Column, Field, select
from sqlmodel import Session as SQLModelSession

from slumber import CONDITIONS_DIR
from slumber.models.base import BaseTable
from slumber.models.dag import CollectionConfig
from slumber.models.gui import GUIConfig
from slumber.utils.database import engine
from slumber.utils.helpers import load_yaml

CONDITION_CONFIG_FILE_EXTENSION = "yaml"


class Condition(BaseTable, table=True):
    __tablename__ = "condition"

    name: str = Field(unique=True)
    gui: dict[str, Any] = Field(sa_column=Column(JSON), exclude=True)
    dag: dict[str, Any] = Field(sa_column=Column(JSON), exclude=True)

    @property
    def gui_config(self) -> GUIConfig:
        return GUIConfig.model_validate(self.gui)

    @property
    def dag_config(self) -> CollectionConfig:
        return CollectionConfig.model_validate(self.dag)


def get_condition_by_name(condition_name: str) -> Condition | None:
    with SQLModelSession(engine) as session:
        return session.exec(
            select(Condition).where(Condition.name == condition_name)
        ).first()


def get_condition_by_id(condition_id: int) -> Condition | None:
    with SQLModelSession(engine) as session:
        return session.exec(
            select(Condition).where(Condition.id == condition_id)
        ).first()


def upsert_conditions_from_configs() -> None:
    for filename in CONDITIONS_DIR.iterdir():
        if filename.suffix != f".{CONDITION_CONFIG_FILE_EXTENSION}":
            logger.info(f"Skipping non-condition config file: {filename}")
            continue

        logger.info(f"Processing condition config file: {filename}")
        config_name = filename.stem
        loaded_condition = Condition.model_validate(load_condition_file(config_name))
        condition = get_condition_by_name(loaded_condition.name)

        if condition:
            logger.debug(
                f"Condition {condition.name} already exists in database. Updating..."
            )
            condition.gui = loaded_condition.gui
            condition.dag = loaded_condition.dag
        else:
            logger.info(f"Condition {condition.name} not found in database. Adding...")
            condition = loaded_condition

        with SQLModelSession(engine) as session:
            session.add(condition)
            session.commit()
            session.refresh(condition)

        logger.info(f"Condition {condition.name} added to database.")


def load_condition_file(config_name: str) -> dict[str, Any]:
    config_file = CONDITIONS_DIR / f"{config_name}.{CONDITION_CONFIG_FILE_EXTENSION}"
    if not config_file.exists():
        raise FileNotFoundError(f"Condition config file {config_file} does not exist.")

    return load_yaml(config_file)
