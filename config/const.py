import os
import pygame

# A
ANIMATION_SPEED = 100

# B
BOMB_COUNT = 1
BOMB_RANGE = 2

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
    "player1": 3,
    "player2": 3,
    "EnemyBat": 1,
}
ENTITY_SPEED = {
    "player1": 1,
    "player2": 1,
    "EnemyBat": 1,
}
ENEMY_MOVE_COOLDOWN = 0
ENEMY_MOVE_DELAY = 30
ENEMY_MIN_NUMBER = 2
ENEMY_SPAWN_MIN_DISTANCE = 4  # distância de Manhattan até o spawn dos jogadores
ENEMY_MAX_NUMBER = 6
EXPLOSION_TIMER = 180
EXPLOSION_DURATION = 45
EXPLOSION_ANIMATION_SPEED = 75

# G
GAME_TITLE = "miniBOMBERMAN"
GRID_LENGTH = 15
GRID_HEIGHT = 15

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
PLAYER_MOVE_COOLDOWN = 20
PLAYER_INVINCIBILITY_TIME = 2000  # ms após levar dano; precisa cobrir a explosão (45 frames ≈ 750 ms)
PLAYER_MOVE_DELAY = 300
PLAYER_SPAWN_COORDS = {
    'player1': (1, 1),
    'player2': (13, 13)
}

# S
STAGE_SCREEN_TIME = 4000

# T
TICK_VALUE = 60
TILE_SIZE = 32

# V
VICTORY_ANIMATION_SPEED = 60
VICTORY_SCREEN_TIME = 5000

# W
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480

# COMPOSITE O
OFFSET_X = (WINDOW_WIDTH - (GRID_LENGTH * TILE_SIZE)) // 2
OFFSET_Y = (WINDOW_HEIGHT - (GRID_HEIGHT * TILE_SIZE)) // 2
