from pathlib import Path

BASE_DIR = Path(__file__).parent

# Change these values if your PostgreSQL user/password/database are different.
# Before running the game, create database snake_db in psql:
# CREATE DATABASE snake_db;
DB_CONFIG = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": 5432,
}

SETTINGS_FILE = BASE_DIR / "settings.json"
ASSETS_DIR = BASE_DIR / "assets"
