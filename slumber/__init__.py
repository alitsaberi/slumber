import importlib.resources
from pathlib import Path

from slumber.utils.helpers import load_yaml

CONFIGS_DIR: Path = importlib.resources.files("configs")
CONDITIONS_DIR = CONFIGS_DIR / "conditions"

_SETTINGS_FILE = CONFIGS_DIR / "settings.yaml"
settings = load_yaml(_SETTINGS_FILE)
