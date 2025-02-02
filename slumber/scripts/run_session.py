import argparse
import os
from pathlib import Path

import ezmsg.core as ez
from loguru import logger

from slumber import settings
from slumber.dag.utils import CollectionConfig
from slumber.utils.helpers import load_yaml
from slumber.utils.logger import setup_logging
from slumber.utils.time import datetime_to_str, now

RUNS_DIR = "sessions"
CONFIGS_DIR = "configs"
LOGS_DIR = "logs"
DATA_DIR = "data"
RUN_DIR_SUBDIRECTORIES = [LOGS_DIR, DATA_DIR]
RUN_NAME_TIME_SEPARATOR = "-"


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


def _create_run_subdirectories(run_directory: Path) -> None:
    for subdirectory_name in RUN_DIR_SUBDIRECTORIES:
        subdirectory = run_directory / subdirectory_name
        subdirectory.mkdir()
        logger.info(f"Created {subdirectory_name} directory: {subdirectory}")


def _create_run_directory(experiment_path: Path, config_name: str) -> Path:
    runs_directory = experiment_path / RUNS_DIR

    if not runs_directory.exists():
        logger.info("Runs directory does not exist. Creating...")
        runs_directory.mkdir()

    datetime_string = datetime_to_str(
        now(time_zone=None), time_separator=RUN_NAME_TIME_SEPARATOR
    )
    run_name = f"{config_name}_{datetime_string}"
    directory = runs_directory / run_name

    if directory.exists():
        raise FileExistsError(f"Run directory {directory} already exists.")

    directory.mkdir()
    logger.info(f"Created run directory: {directory}")

    _create_run_subdirectories(directory)

    return directory


def _get_config_file(experiment_path: Path, config_name: str) -> Path:
    config_file = experiment_path / CONFIGS_DIR / f"{config_name}.yaml"
    if not config_file.exists():
        raise FileNotFoundError(f"Config file {config_file} does not exist.")
    return config_file.absolute()


def _setup_logging(run_directory: Path) -> None:
    logs_dir = run_directory / LOGS_DIR
    setup_logging(logs_dir, settings["logging"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an experiment session.")
    parser.add_argument(
        "experiment_path", type=Path, help="Path to the experiment directory"
    )
    parser.add_argument(
        "config_name", type=str, help="Name of the experiment config file"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    config_file = _get_config_file(args.experiment_path, args.config_name)
    run_directory = _create_run_directory(args.experiment_path, args.config_name)
    _setup_logging(run_directory)
    os.chdir(run_directory)

    # initialize_db()

    session_config = CollectionConfig.model_validate(load_yaml(config_file))
    # insert_default_configs(**asdict(session_config.components["GUI"].SETTINGS))
    logger.info(
        f"Running collection {session_config.name if session_config.name else ''}"
        f": Components: {list(session_config.components.keys())}"
        f" - {len(session_config.connections)} connections"
        f" - Process components: {list(session_config.process_components)}"
    )
    ez.run(**session_config.model_dump(by_alias=True))


if __name__ == "__main__":
    main()
