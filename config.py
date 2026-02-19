# cli/config.py
import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".kodeka" / "config.json"
CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

DEFAULT_CONFIG = {
    "provider": None,
    "api_key": "",
    "model": None,
    "theme": "default"  # future use
}

def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                data = json.load(f)
                default = DEFAULT_CONFIG.copy()
                default.update(data)
                return default
        except:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def ensure_config_exists():
    if not CONFIG_PATH.exists():
        save_config(DEFAULT_CONFIG)
