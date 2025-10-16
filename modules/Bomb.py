import os
from typing import Tuple

import pygame
from config.const import EXPLOSION_TIMER, PATH_ITEMS, PATH_SOUNDS
from modules.AnimationManager import AnimationManager
from modules.Entity import Entity, EntityType


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
        self.timer = EXPLOSION_TIMER
        self.exploded = False

        # animações
        self.animation_manager = AnimationManager()
        self.load_animations()

        # som
        self.place_sound = pygame.mixer.Sound(os.path.join(PATH_SOUNDS, 'place_bomb.wav'))
        self.place_sound.play()


    def load_animations(self):
        """Carrega a animação da bomba"""
        self.animation_manager.load_animation("bomb", PATH_ITEMS, 9, "dynamite_{}.png")
        self.animation_manager.set_animation("bomb")

    def update(
        self, 
        game
    ):
        current_time = pygame.time.get_ticks()

        self.timer -= 1
        if self.timer <= 0:
            self.explode(game)
        else:
            self.animation_manager.animation_speed = max(50, 200 - (180 - self.timer) * 2)
            self.animation_manager.update(current_time)

    def explode(
        self,
        game,
    ):
        self.exploded = True
        self.alive = False

        from modules.EntityFactory import EntityFactory
        explosion = EntityFactory.create_explosion(
            self.position,
            self.explosion_range,
            self.owner
        )

        game.entity_manager.add_entity(explosion)

    def render(self, screen, offset_x: int, offset_y: int, tile_size: int):
        pixel_x = self.position[0] * tile_size + offset_x
        pixel_y = self.position[1] * tile_size + offset_y
        
        current_frame = self.animation_manager.get_current_frame()
        
        if current_frame.get_size() != (tile_size, tile_size):
            current_frame = pygame.transform.scale(current_frame, (tile_size, tile_size))
        
        screen.blit(current_frame, (pixel_x, pixel_y))