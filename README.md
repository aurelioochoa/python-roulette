# Python Roulette

A terminal-based Russian Roulette game for 2 players with ASCII animations, sound effects, and colored logging.

## Features

- **Interactive Mode** — Full experience with ASCII animations, sound effects, and user input
- **Automatic Mode** — AI plays both sides with logs only (no graphics/sound)
- **Configurable Difficulty** — 1-6 bullets per round (default: 1)
- **3 Lives per Player** — Survive multiple hits before elimination
- **ASCII Art Animations** — Drum display, spinning, and firing sequences
- **Sound Effects** — Gunshots, dry fire clicks, drum spin, and more
- **Colored Logging** — Timestamped game events with ANSI colors
- **Game Records** — Automatically saved to `records/` directory

## Project Structure

```
pythonRoulette/
├── source/
│   ├── game.py  # Main game orchestrator
│   ├── revolver.py         # Revolver class (drum, loading, firing)
│   ├── player.py           # Player class (lives, shooting)
│   ├── crupier.py          # Crupier class (game setup)
│   ├── graphics.py         # ASCII animations
│   ├── logger.py           # Colored logging system
│   ├── soundEffects.py     # Audio playback (pygame)
│   └── tests.py            # Unit tests (59 tests)
├── sfx/                    # Sound effect files (.mp3)
├── records/                # Game records (auto-generated)
├── Dockerfile
└── docker-compose.yml
```

## Installation

### Requirements
- Python 3.11+
- pygame >= 2.5.0 (optional, for sound)

### Install Dependencies
```bash
pip install -r source/requirements.txt
```

## Usage

### Run the Game
```bash
python3 source/game.py
```

### Mode Selection
```
🔫 PYTHON ROULETTE 🔫

Select mode:
  1. Interactive (with graphics and sound)
  2. Automatic (logs only)
```

### Run Tests
```bash
cd source
python3 -m unittest tests -v
```

## Game Mechanics

### Chamber States
```
[ ] — Empty chamber
[O] — Live bullet
[@] — Fired cartridge
```

### Drum Layout
```
   _________
  /         \
 /    [5]    \
 | [4]   [0] |
 | [3]   [1] |
 \    [2]    /
  \_________/
```

### Turn Flow
1. Crupier loads bullets and spins the drum
2. Player takes the revolver
3. Player chooses: shoot themselves or opponent
4. Pull trigger → BANG! or *click*
5. Pass to next player
6. When drum is empty, new round begins
7. Last player standing wins

## Docker

### Build and Run
```bash
docker build -t python-roulette .
docker run -it -v ./records:/app/records -v /etc/localtime:/etc/localtime:ro python-roulette
```

### With Sound (PulseAudio)
```bash
docker run -it \
  -v ./records:/app/records \
  -v /run/user/1000/pulse:/run/user/1000/pulse \
  -v /etc/localtime:/etc/localtime:ro \
  -e PULSE_SERVER=unix:/run/user/1000/pulse/native \
  --device /dev/snd \
  --group-add audio \
  python-roulette
```

## License

MIT# python-roulette
