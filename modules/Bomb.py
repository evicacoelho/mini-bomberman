import os
from typing import Tuple

import pygame
from config.const import EXPLOSION_TIMER, PATH_ITEMS, PATH_SOUNDS
from modules.AnimationManager import AnimationManager
from modules.assets import load_sound
from modules.Entity import Entity, EntityType
from modules.Explosion import Explosion


class Bomb(Entity):
    def __init__(
        self, 
        position: Tuple[int, int],
        explosion_range: int,
        owner,
    ):
        super().__init__("Bomb", position, EntityType.BOMB)
        self.explosion_range = explosion_range
        self.owner = owner
        self.placed_at = pygame.time.get_ticks()
        self.exploded = False

        # animações
        self.animation_manager = AnimationManager()
        self.animation_manager.load_animation("bomb", PATH_ITEMS, 9, "dynamite_{}.png")

        # som
        load_sound(os.path.join(PATH_SOUNDS, 'place_bomb.wav')).play()

    def update(
        self, 
        game
    ):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.placed_at

        if elapsed >= EXPLOSION_TIMER:
            self.explode(game)
        else:
            # pavio acelera: 200 ms por quadro, caindo até 50 ms
            self.animation_manager.animation_speed = max(50, 200 - elapsed // 8)
            self.animation_manager.update(current_time)

    def explode(
        self,
        game,
    ):
        self.exploded = True
        self.alive = False
        game.entity_manager.add_entity(
            Explosion(self.position, self.explosion_range, self.owner, game)
        )
