import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")
LEADERBOARD_FILE = Path("leaderboard.json")

DEFAULT_SETTINGS = {"sound": True, "car_color": "blue", "difficulty": "normal"}
DEFAULT_LEADERBOARD = []


def load_settings():
    # If file is missing or broken, I use default settings.
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


def load_leaderboard():
    # Leaderboard is a simple list of dictionaries.
    if not LEADERBOARD_FILE.exists():
        save_leaderboard(DEFAULT_LEADERBOARD)
        return DEFAULT_LEADERBOARD.copy()
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list):
            return data
        return DEFAULT_LEADERBOARD.copy()
    except (json.JSONDecodeError, OSError):
        save_leaderboard(DEFAULT_LEADERBOARD)
        return DEFAULT_LEADERBOARD.copy()


def save_leaderboard(scores):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


def add_score(username, score, distance, coins):
    scores = load_leaderboard()
    scores.append({
        "name": username,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })
    # Best score goes first. Distance is used if two scores are close.
    scores.sort(key=lambda item: (item["score"], item["distance"]), reverse=True)
    scores = scores[:10]
    save_leaderboard(scores)
    return scores
