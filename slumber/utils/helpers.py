from pathlib import Path

import yaml


def load_yaml(config_path: Path) -> dict:
    """Load a yaml file and return the contents as a dictionary.

    Args:
        config_path (Path): Path to the yaml file.

    Returns:
        dict: The contents of the yaml file.
    """
    with open(config_path) as file:
        config = yaml.safe_load(file)
    return config
