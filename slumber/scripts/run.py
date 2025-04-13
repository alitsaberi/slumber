import argparse

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from slumber.gui.main_window import MainWindow
from slumber.sources.zmax import close_all_hypnodyne_processes
from slumber.utils.logger import setup_logging

DAG_LOG_FILE_NAME = "dag.log"
GUI_LOG_FILE_NAME = "gui.log"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an experiment session.")
    parser.add_argument(
        "--full-screen",
        action="store_true",
        help="Run in full screen mode",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    setup_logging()

    app = QApplication()
    window = MainWindow()

    if args.full_screen:
        window.setWindowFlag(Qt.WindowStaysOnTopHint)
        window.showFullScreen()
    else:
        window.show()

    try:
        app.exec()
    finally:
        close_all_hypnodyne_processes()


if __name__ == "__main__":
    main()
