# miniBOMBERMAN

A small grid-based bomb arena game made with Python and pygame. Blow up boxes, trap the bats with your bombs, and clear all four stages, alone or with a friend on the same keyboard.

## Running

Requires **Python 3.12+**.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Run it from the repository root: asset paths are relative to the current directory.

## How to play

Each stage is a 15×15 arena. Destroy every enemy to move on to the next stage. Bombs explode in a cross, stop at solid blocks and break the first box they hit. Bombs also block movement, so you can use them to corner enemies.

You have 3 lives. After a hit you blink and are invincible for 2 seconds. Lose all your lives and it's game over. Clear all 4 stages to see the victory screen.

| Action     | Player 1     | Player 2      |
| ---------- | ------------ | ------------- |
| Move       | W A S D      | Arrow keys    |
| Bomb       | Left Shift   | Right Shift   |
| Back to menu | Esc        | Esc           |

## Project layout

```
main.py              menu → stages → victory loop
config/const.py      all tuning values: speeds, timers (ms), lives, controls, paths
config/levels.py     stage layouts (0 = ground, 1 = block, 2 = box) and tile themes
modules/
  Game.py            one stage: map, entity spawning, game loop, HUD
  Entity.py          base class for everything on the map
  Player.py  Enemy.py  Bomb.py  Explosion.py
  EntityManager.py   updates, draws and checks collisions between entities
  AnimationManager.py  sprite animation frames
  assets.py          cached image and sound loading
  Menu.py  Victory.py  screens
assets/              sprites, tiles, backgrounds and sounds
test_explosion.py    checks the explosion range rules
```

### Adding a stage

Add a new entry to `LEVELS` in `config/levels.py` with a 15×15 `layout` and pick the `terrain` and `block` image sets from `assets/terrain` (`variations` is how many numbered images that set has). Stages are played in key order. No code changes needed.

## Tests

```bash
python test_explosion.py
```

## Building an executable

```bash
pip install -r requirements-build.txt
```

Builds are made with PyInstaller. Since assets are loaded relative to the current directory, keep the `assets/` folder next to the executable and launch it from that folder.
