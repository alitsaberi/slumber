import importlib.resources

from slumber.utils.helpers import load_yaml

CONFIGS_DIR = importlib.resources.files("configs")
_SETTINGS_FILE = CONFIGS_DIR / "settings.yaml"

settings = load_yaml(_SETTINGS_FILE)
