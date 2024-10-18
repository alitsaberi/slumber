import importlib.resources

from slumber.utils.helpers import load_yaml

_CONFIGS_DIR = importlib.resources.files("configs")
_SETTINGS_FILE = _CONFIGS_DIR / "settings.yaml"

settings = load_yaml(_SETTINGS_FILE)
