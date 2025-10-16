import random

from config.const import ENEMY_MOVE_COOLDOWN, ENEMY_MOVE_DELAY
from modules.Entity import Entity, EntityType


class Enemy(Entity):
    def __init__(
        self, 
        name, 
        position
    ):
        super().__init__(name, position, EntityType.ENEMY, speed=1)
        self.move_cooldown = ENEMY_MOVE_COOLDOWN
        self.move_delay = ENEMY_MOVE_DELAY

    def update(self, game):
        self.move_cooldown -= 1
        if self.move_cooldown <= 0:
            self.random_move(game)
            self.move_cooldown = self.move_delay

    def random_move(self, game):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        random.shuffle(directions)
        
        current_x, current_y = self.position
        
        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy
            if game.is_walkable(new_x, new_y):
                self.position = (new_x, new_y)
                break
