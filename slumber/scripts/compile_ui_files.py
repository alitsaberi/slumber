import argparse
import subprocess
from pathlib import Path

from loguru import logger

UI_EXTENSION = "ui"
COMPILED_FILE_NAME_FORMAT = "{}_ui.py"

# TODO: check if it's possible to load ui files directly

def _compile_ui(ui_file: Path, output_file: Path) -> None:
    command = f"pyside6-uic {ui_file} -o {output_file}"
    subprocess.run(command, shell=True, check=True)
    logger.info(f"Compiled {ui_file} → {output_file}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new task.")
    parser.add_argument(
        "directory", type=Path, help="Path to directory containing UI files"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    
    if not args.directory.is_dir():
        raise NotADirectoryError(f"{args.directory} is not a directory")
    
    for ui_file in args.directory.rglob(f"*.{UI_EXTENSION}"):
        output_file = ui_file.parent / COMPILED_FILE_NAME_FORMAT.format(ui_file.stem)
        _compile_ui(ui_file, output_file)
    

if __name__ == "__main__":
    main()
