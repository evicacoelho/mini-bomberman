import os
from typing import List, Self, Tuple

import pygame
from config.const import EXPLOSION_ANIMATION_SPEED, EXPLOSION_DURATION, PATH_FXS, PATH_SOUNDS
from modules.AnimationManager import AnimationManager
from modules.Entity import Entity, EntityType
from modules.TileType import TileType


def calculate_affected_tiles(center, explosion_range, tile_at) -> List[Tuple[int, int]]:
    """Cruz a partir do centro: para antes de BLOCK, inclui o primeiro BOX e para nele."""
    cx, cy = center
    affected = [(cx, cy)]
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        for i in range(1, explosion_range + 1):
            tile = (cx + dx * i, cy + dy * i)
            kind = tile_at(*tile)
            if kind == TileType.BLOCK:
                break
            affected.append(tile)
            if kind == TileType.BOX:
                break
    return affected


class Explosion(Entity):
    def __init__(
        self,  
        position: int, 
        explosion_range: int, 
        owner,
        game,
    ):
        super().__init__("Explosion", position, EntityType.EXPLOSION)
        self.explosion_range = explosion_range
        self.owner = owner
        self.duration = EXPLOSION_DURATION
        self.affected_tiles = calculate_affected_tiles(position, explosion_range, game.get_tile_at_position)

        # animações
        self.animation_manager = AnimationManager()
        self.load_animations()

        # sons
        self.explosion_sound = pygame.mixer.Sound(os.path.join(PATH_SOUNDS, 'bomb_explodes.wav'))
        self.explosion_sound.play()

    def load_animations(self):
        self.animation_manager.load_animation("explosion", PATH_FXS, 6, "explosion_{}.png")
        self.animation_manager.set_animation("explosion")
        self.animation_manager.animation_speed = EXPLOSION_ANIMATION_SPEED

    def update(self, game):
        current_time = pygame.time.get_ticks()
        self.duration -= 1

        self.animation_manager.update(current_time)

        if self.duration <= 0:
            self.alive = False

    def render(
        self,
        screen,
        offset_x: int,
        offset_y: int,
        tile_size: int,
    ):
        current_frame = self.animation_manager.get_current_frame()
        
        if self.duration < 15:  # Últimos 15 frames
            alpha = int(255 * (self.duration / 15))
            current_frame.set_alpha(alpha)
        
        for grid_x, grid_y in self.affected_tiles:
            pixel_x = grid_x * tile_size + offset_x
            pixel_y = grid_y * tile_size + offset_y
            
            # Escala a imagem para o tamanho do tile se necessário
            scaled_frame = current_frame
            if current_frame.get_size() != (tile_size, tile_size):
                scaled_frame = pygame.transform.scale(current_frame, (tile_size, tile_size))
            
            screen.blit(scaled_frame, (pixel_x, pixel_y))