import argparse
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from ruamel.yaml import YAML

from slumber import settings

TEMPLATES_DIR = Path(__file__).parent.parent / "gui" / "pages" / "tasks"
TASKS_DIR_NAME = "tasks"
ASSETS = ["html/index.html", "css/styles.css", "js/script.js"]


def _create_assets_directory(task_directory: Path, html_support: bool) -> None:
    assets_directory = task_directory / "assets"
    assets_directory.mkdir()
    logger.info(f"Created assets directory: {assets_directory}")

    if not html_support:
        return

    for asset in ASSETS:
        file_path = assets_directory / asset
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()
            logger.info(f"Created file: {file_path}")


def _copy_template_files(
    template_directory: Path, task_directory: Path, name: str, header: str
) -> None:
    environment = Environment(loader=FileSystemLoader(template_directory))

    for template_file in template_directory.iterdir():
        if not template_file.is_file():
            logger.debug(f"Skipping non-file: {template_file}")
            continue

        template = environment.get_template(template_file.name)
        output_content = template.render(name=name, header=header)
        output_path = task_directory / template_file.name

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)

        logger.info(f"Created {output_path}")


def _create_tasks_directory(experiment_path: Path) -> Path:
    tasks_directory = experiment_path / TASKS_DIR_NAME

    if not tasks_directory.exists():
        logger.info("Tasks directory does not exist. Creating...")
        tasks_directory.mkdir()

    return tasks_directory


def _create_task_directory(tasks_directory: Path, name: str) -> Path:
    task_directory = tasks_directory / name

    if task_directory.exists():
        raise FileExistsError(f"Task directory {task_directory} already exists.")

    task_directory.mkdir()
    logger.info(f"Created task directory: {task_directory}")
    return task_directory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new task.")
    parser.add_argument(
        "experiment_path", type=Path, help="Path to the experiment directory"
    )
    parser.add_argument(
        "--template",
        type=str,
        help="Name of the template to use",
        default=settings["tasks"]["default"],
    )
    return parser.parse_args()


def main():
    args = parse_args()
    tasks_directory = _create_tasks_directory(args.experiment_path)

    name = input("Task name: ")
    header = input("Task page header: ")
    directory_name = name.lower().replace(" ", "_").replace("-", "_")

    task_directory = _create_task_directory(tasks_directory, directory_name)
    template_directory = TEMPLATES_DIR / args.template

    if not template_directory.exists():
        raise FileNotFoundError(
            f"Template directory {template_directory} does not exist."
        )

    _copy_template_files(template_directory, task_directory, name, header)

    html_support = input("Need HTML support? (y/n): ").strip().lower() in ["y", "yes"]

    if html_support:
        _create_assets_directory(task_directory, html_support)

    logger.info(f"Task was created at: {task_directory}")


if __name__ == "__main__":
    main()
