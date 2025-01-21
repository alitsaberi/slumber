import asyncio
import os
import sys
from datetime import datetime, timedelta

import qasync
import yaml
from PySide6.QtWidgets import QApplication

from .gui.main_window import MainWindow
from .model.gui_config_model import (
    get_gui_config,
    insert_default_gui_config,
)
from .model.study_calendar_model import populate_study_calendar
from .model.study_config_model import get_study_config, insert_study_config
from .model.task_progress_model import populate_task_progress
from .model.tasks_model import get_tasks, insert_task
from .utils.db_utils import initialize_db

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


def read_yaml_config(file_path):
    with open(file_path) as file:
        config = yaml.safe_load(file)
    return config

def insert_default_configs(yaml_config):
    # Insert default GUI config if not exists
    gui_config = get_gui_config()
    if gui_config is None:
        print("No GUI config found, inserting default GUI config")
        gui_config = yaml_config['gui_config']
        insert_default_gui_config(
            gui_config['font_size'],
            gui_config['app_width'],
            gui_config['app_height'],
            gui_config['app_mode'],
            gui_config['language']
        )

    # Insert default study config if not exists and populate study calendar
    study_config = get_study_config()
    if study_config is None:
        study_config_yaml = yaml_config['study_config']
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=study_config_yaml['duration'])
        insert_study_config(study_config_yaml['duration'], start_date, end_date)
        populate_study_calendar(study_config_yaml['duration'], start_date)

     # Insert default tasks if not exists
    tasks = get_tasks()
    if not tasks:
        print("No tasks found, inserting default tasks")
        procedure_tasks = yaml_config['procedure_tasks']
        for task in procedure_tasks:
            insert_task(task['name'], task['header'], task['module'], task['type'])

        # Populate task progress if not exists
        populate_task_progress()
   

def main():
    # Read YAML config
    config_dir = os.path.dirname(__file__)
    yaml_config_path = os.path.join(config_dir, '../configs/settings.yaml')
    yaml_config = read_yaml_config(yaml_config_path)

    # Initialize the database
    initialize_db()

    # Insert default configs if not exists
    insert_default_configs(yaml_config)

    # Retrieve the updated setup
    print(get_gui_config())
    gui_config = get_gui_config()
    study_config = get_study_config()
    tasks = get_tasks()

    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create the qasync event loop
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Initialize and show the main window
    window = MainWindow(gui_config, study_config, tasks)
    window.show()

    # Instead of sys.exit(app.exec()), run the integrated asyncio event loop
    with loop:
        sys.exit(loop.run_forever())

if __name__ == "__main__":
    main()