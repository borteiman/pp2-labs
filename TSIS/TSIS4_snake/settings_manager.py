import json
from config import SETTINGS_FILE

DEFAULT_SETTINGS = {
    "snake_color": [60, 180, 95],
    "grid": True,
    "sound": True,
}


def load_settings():
    # If settings.json does not exist, I create it with default values.
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(data)

        return settings

    except (json.JSONDecodeError, OSError):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)
