from pathlib import Path

from slumber.utils.helpers import load_yaml

BASE_DIR = Path(__file__).parent.parent
CONFIGS_DIR = BASE_DIR / "configs"
CONDITIONS_DIR = CONFIGS_DIR / "conditions"
MODELS_DIR = CONFIGS_DIR / "models"
SESSIONS_DIR = BASE_DIR / "sessions"

_SETTINGS_FILE = CONFIGS_DIR / "settings.yaml"
settings = load_yaml(_SETTINGS_FILE)
