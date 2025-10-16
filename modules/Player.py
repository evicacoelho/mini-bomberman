from typing import Any, List, Tuple

import pygame
from config.const import CONTROLS, ENTITY_SPEED
from modules.Entity import Entity, EntityType
from modules.Game import Game


class Player(Entity):
    def __init__(
        self, 
        name: str, 
        position: Tuple[int, int], 
        player_number: int = 1,
    ):
        super().__init__(name, position, EntityType.PLAYER, speed=ENTITY_SPEED[name])
        self.name = name
        self.player_number = player_number,
        self.alive = True
        self.lives = 3,
        self.bomb_count = 1,
        self.bomb_range = 3,
        self.placed_bombs: List[Any]

        # controles
        self.controls = CONTROLS[self.name]

        def update(
            self,
            game: Game
        ):
            keys = pygame.key.get_pressed()
            grid_x, grid_y = self.position

            new_x, new_y = grid_x, grid_y

            if keys[self.controls['up']]:
                new_y -= self.speed
            if keys[self.controls['down']]:
                new_y += self.speed
            if keys[self.controls['left']]:
                new_x -= self.speed
            if keys[self.controls['up']]:
                new_x += self.speed

            if game.is_walkable(new_x, new_y):
                self.position = (new_x, new_y)

            if keys[self.controls['bomb']] and len(self.placed_bombs) <  self.bomb_count:
                self.place_bomb(game)

        def place_bomb(
            self,
            game: Game
        ):
            from modules.EntityFactory import EntityFactory
            bomb = EntityFactory.create_bomb(self.position, self.bomb_range, self)
            
            self.placed_bombs.append(bomb)
            game.entity_manager.add_entity(bomb)

        def lose_life(self) -> bool:
            self.lives -= 1
            if self.lives <= 0:
                self.alive = False
            
            return self.lives <= 0
