from enum import Enum


class EntityType(Enum):
    PLAYER = 'player'
    ENEMY = 'enemy'
    BOMB = 'bomb'
    EXPLOSION = 'explosion'