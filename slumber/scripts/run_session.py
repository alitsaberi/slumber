import argparse
import os
from multiprocessing import Pipe, Process
from pathlib import Path

import ezmsg.core as ez
from loguru import logger
from PySide6.QtWidgets import QApplication

from slumber import CONDITIONS_DIR
from slumber.gui.main_window import MainWindow
from slumber.models.condition import Condition
from slumber.models.dag import CollectionConfig
from slumber.sources.zmax import open_server
from slumber.utils.helpers import load_yaml
from slumber.utils.logger import setup_logging
from slumber.utils.time import create_timestamped_name

SESSIONS_DIR = Path("./sessions")
LOGS_DIR_NAME = "logs"
DATA_DIR_NAME = "data"
RUN_DIR_SUBDIRECTORIES = [LOGS_DIR_NAME, DATA_DIR_NAME]
CONDITION_CONFIG_FILE_EXTENSION = "yaml"
HDSERVER_LOG_FILE_NAME = "hdserver.log"
DAG_LOG_FILE_NAME = "dag.log"
MAIN_LOG_FILE_NAME = "slumber.log"
PROCESS_TERMINATION_TIMEOUT = 5.0


def _run_dag(
    dag_config: CollectionConfig,
    logs_dir: Path,
) -> None:
    setup_logging(logs_dir / DAG_LOG_FILE_NAME)
    ez.run(**dag_config.model_dump(by_alias=True))


def _setup_dag_process(
    dag_config: CollectionConfig,
    logs_dir: Path,
) -> Process:
    logger.info(f"Creating the DAG process: {dag_config}")

    return Process(
        target=_run_dag,
        args=(
            dag_config,
            logs_dir,
        ),
        name="dag_process",
    )


def _setup_pipe_connections(condition_config: dict) -> None:
    parent_connection, child_connection = Pipe()
    condition_config["dag"]["components"]["MASTER"]["settings"]["gui_connection"] = (
        child_connection
    )
    condition_config["gui"]["dag_connection"] = parent_connection


def _get_condition(config_name: str) -> Condition:
    config_file = CONDITIONS_DIR / f"{config_name}.{CONDITION_CONFIG_FILE_EXTENSION}"
    if not config_file.exists():
        raise FileNotFoundError(f"Condition config file {config_file} does not exist.")

    condition_config = load_yaml(config_file)
    _setup_pipe_connections(condition_config)

    return Condition.model_validate(condition_config)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an experiment session.")
    parser.add_argument(
        "condition_config_file",
        type=str,
        help="Name of the condition config file for the session",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    condition = _get_condition(args.condition_config_file)

    run_directory = _create_run_directory(condition.name)
    logs_dir = run_directory / LOGS_DIR_NAME
    setup_logging(logs_dir / MAIN_LOG_FILE_NAME)

    os.chdir(run_directory)

    dag_process = _setup_dag_process(condition.dag, logs_dir)

    app = QApplication()
    window = MainWindow(gui_config=condition.gui, dag_process=dag_process)

    window.show()

    hdserver_process = open_server(logs_dir / HDSERVER_LOG_FILE_NAME)

    try:
        app.exec()
    finally:
        if dag_process.is_alive():
            logger.info("Terminating the DAG process...")
            dag_process.terminate()
            dag_process.join(timeout=PROCESS_TERMINATION_TIMEOUT)
            if dag_process.is_alive():
                dag_process.kill()

        logger.info("Terminating the HDServer process...")
        hdserver_process.terminate()


if __name__ == "__main__":
    main()
