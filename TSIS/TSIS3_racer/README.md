# TSIS 3 Racer Game

Run:

```bash
python3 main.py
```

Files:

- `main.py` - screen switching and main loop
- `racer.py` - gameplay, sprites, collisions, scoring
- `ui.py` - menu, settings, leaderboard, game over screens
- `persistence.py` - loading and saving JSON files
- `settings.json` - saved sound, car color, difficulty
- `leaderboard.json` - saved top 10 scores
- `assets/` - optional folder for images/sounds

Controls:

- Left / Right arrows or A / D - move car
- Escape - return to main menu while playing
- Mouse - click menu buttons

Features:

- Lane hazards and safe paths
- Dynamic road events
- Traffic cars and road obstacles
- Weighted coins
- Nitro, Shield, Repair power-ups
- Difficulty scaling
- Distance meter and finish distance
- Score based on distance, coins, and power-up bonuses
- Username entry
- Persistent leaderboard
- Persistent settings
