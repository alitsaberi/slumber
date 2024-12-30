import sys
import os
import yaml
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from utils.db_utils import initialize_db
from model.gui_config_model import get_gui_config

def read_yaml_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    # Read and print the YAML config
    yaml_config_path = os.path.join(os.path.dirname(__file__), '../configs/settings.yaml')
    yaml_config = read_yaml_config(yaml_config_path)
    print("YAML Config:")
    print(yaml_config)

    # Initialize the database
    initialize_db()

    # Insert default config if not exists
    config = get_gui_config()
    if config is None:
        print("No config found, inserting default config")

    print("Config:")
    print(config)

    # Start the GUI
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()