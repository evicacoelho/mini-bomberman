import os
import pygame

# B

# C
CONTROLS = {
    'player1': {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'left': pygame.K_a,
        'right': pygame.K_d,
        'bomb': pygame.K_LSHIFT
    },
    'player2': {
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'bomb': pygame.K_RSHIFT
    }
}

# E
ENTITY_HEALTH = {
    "Player1": 1,
    "Player2": 1,
    "EnemyBat": 1,
}
ENTITY_SPEED = {
    "Player1": 3,
    "Player2": 3,
    "EnemyBat": 1,
}
ENEMY_MOVE_COOLDOWN = 0
ENEMY_MOVE_DELAY = 30
EXPLOSION_TIMER = 180
EXPLOSION_DURATION = 45

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
PATH_SOUNDS = os.path.join(PATH_ASSETS, 'sounds')
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
