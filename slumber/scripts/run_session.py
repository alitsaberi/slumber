import argparse
import os
from pathlib import Path

import ezmsg.core as ez
from loguru import logger

from slumber import settings
from slumber.dag.utils import CollectionConfig
from slumber.utils.helpers import load_yaml
from slumber.utils.logger import setup_logging
from slumber.utils.time import create_timestamped_name

SESSIONS_DIR = Path("./sessions")
CONFIGS_DIR = Path("./configs")
CONDITIONS_DIR = CONFIGS_DIR / "conditions"
LOGS_DIR_NAME = "logs"
DATA_DIR_NAME = "data"
RUN_DIR_SUBDIRECTORIES = [LOGS_DIR_NAME, DATA_DIR_NAME]
CONDITION_CONFIG_FILE_EXTENSION = "yaml"


# # TODO: should be move to experiment setup
# def insert_default_configs(tasks: list[Task]):
#     gui_config = get_gui_config()
#     if gui_config is None:
#         logger.info("No GUI config found, inserting default GUI config...")
#         insert_default_gui_config(**settings["gui"])

#     study_config = get_study_config()
#     if study_config is None:
#         logger.info("No study config found, updating db...")
#         start_date = now().date()  # should come from the configuration file
#         end_date = start_date + timedelta(days=settings["study"]["duration"])
#         insert_study_config(settings["study"]["duration"], start_date, end_date)
#         populate_study_calendar(settings["study"]["duration"], start_date)

#     if not get_tasks():
#         logger.info("No tasks found, inserting default tasks")
#         for task in tasks:
#             insert_task(**task.model_dump(exclude={"enabled"}))

#         populate_task_progress()


def _get_condition_config_file(config_name: str) -> Path:
    config_file = CONDITIONS_DIR / f"{config_name}.{CONDITION_CONFIG_FILE_EXTENSION}"
    if not config_file.exists():
        raise FileNotFoundError(f"Config file {config_file} does not exist.")
    return config_file.absolute()


def _create_run_subdirectories(run_directory: Path) -> None:
    for subdirectory_name in RUN_DIR_SUBDIRECTORIES:
        subdirectory = run_directory / subdirectory_name
        subdirectory.mkdir()
        logger.info(f"Created {subdirectory_name} directory: {subdirectory}")


def _create_run_directory(config_name: str) -> Path:
    if not SESSIONS_DIR.exists():
        logger.info("Sessions directory does not exist. Creating {SESSIONS_DIR}...")
        SESSIONS_DIR.mkdir()

    directory = SESSIONS_DIR / create_timestamped_name(config_name)

    if directory.exists():
        raise FileExistsError(f"Session directory {directory} already exists.")

    directory.mkdir()
    logger.info(f"Created run directory: {directory}")

    _create_run_subdirectories(directory)

    return directory


def _setup_logging(run_directory: Path) -> None:
    logs_dir = run_directory / LOGS_DIR_NAME
    setup_logging(logs_dir, settings["logging"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an experiment session.")
    parser.add_argument(
        "condition_config_name", type=str, help="Name of the condition config file"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    config_file = _get_condition_config_file(args.condition_config_name)
    run_directory = _create_run_directory(args.condition_config_name)
    _setup_logging(run_directory)
    os.chdir(run_directory)
    
    session_config = CollectionConfig.model_validate(load_yaml(config_file))
    logger.info(
        f"Running collection {session_config.name if session_config.name else ''}"
        f": Components: {list(session_config.components.keys())}"
        f" - {len(session_config.connections)} connections"
        f" - Process components: {list(session_config.process_components)}"
    )
    ez.run(**session_config.model_dump(by_alias=True))


if __name__ == "__main__":
    main()
