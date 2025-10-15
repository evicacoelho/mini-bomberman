import os

# B

# E
ENTITY_HEALTH = {
    "Player1": 1,
    "Player2": 1,
    "EnemyBat": 1,
},

ENTITY_SPEED = {
    "Player1": 3,
    "Player2": 3,
    "EnemyBat": 1,
}

# G
GAME_TITLE = "miniBOMBERMAN"
GRID_LENGTH = 15
GRID_HEIGHT = 15

# I

# O

# P
PATH = os.path.join('')
PATH_ASSETS = os.path.join(PATH, 'assets')
PATH_BACKGROUNDS = os.path.join(PATH_ASSETS, 'backgrounds')
PATH_CHARACTER = os.path.join(PATH_ASSETS, 'character')
PATH_ENEMIES = os.path.join(PATH_ASSETS, 'enemies')
PATH_FXS = os.path.join(PATH_ASSETS, 'fxs')
PATH_ITEMS = os.path.join(PATH_ASSETS, 'items')
PATH_TERRAIN = os.path.join(PATH_ASSETS, 'terrain')

# T
TICK_VALUE = 60
TILE_SIZE = 32

# W
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480

# COMPOSITE O
OFFSET_X = (WINDOW_WIDTH - (GRID_LENGTH * TILE_SIZE)) // 2
OFFSET_Y = (WINDOW_HEIGHT - (GRID_HEIGHT * TILE_SIZE)) // 2
