# TSIS 4 Snake Game

## Requirements

- Python
- pygame
- psycopg2-binary
- PostgreSQL database

Install packages:

```bash
pip install pygame psycopg2-binary
```

Create database in psql:

```sql
CREATE DATABASE snake_db;
```

If your PostgreSQL password is different, edit `config.py`.

Tables are created automatically when the game starts.

## Run

```bash
python3 main.py
```

## Controls

- Arrow keys: move snake
- Escape: return to menu during game
- Mouse: buttons in menu/settings/game over

## Features

- PostgreSQL leaderboard with players and game_sessions tables
- Username entry on main menu
- Personal best shown during game
- Weighted food
- Food disappearing by timer
- Poison food
- Speed, slow motion, shield power-ups
- Obstacles from level 3
- settings.json for snake color, grid overlay and sound
- Main Menu, Game Over, Leaderboard, Settings screens
