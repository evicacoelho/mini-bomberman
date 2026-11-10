import os
from typing import List, Tuple

import pygame
from config.const import (
    EXPLOSION_ANIMATION_SPEED,
    EXPLOSION_DURATION,
    EXPLOSION_FADE_TIME,
    PATH_FXS,
    PATH_SOUNDS,
)
from modules.AnimationManager import AnimationManager
from modules.assets import load_sound
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
        position: Tuple[int, int], 
        explosion_range: int, 
        owner,
        game,
    ):
        super().__init__("Explosion", position, EntityType.EXPLOSION)
        self.explosion_range = explosion_range
        self.owner = owner
        self.created_at = pygame.time.get_ticks()
        self.affected_tiles = calculate_affected_tiles(position, explosion_range, game.get_tile_at_position)

        # animações
        self.animation_manager = AnimationManager()
        self.animation_manager.load_animation("explosion", PATH_FXS, 6, "explosion_{}.png")
        self.animation_manager.animation_speed = EXPLOSION_ANIMATION_SPEED

        # sons
        load_sound(os.path.join(PATH_SOUNDS, 'bomb_explodes.wav')).play()

    def remaining_time(self) -> int:
        return EXPLOSION_DURATION - (pygame.time.get_ticks() - self.created_at)

    def update(self, game):
        self.animation_manager.update(pygame.time.get_ticks())
        if self.remaining_time() <= 0:
            self.alive = False

    def render(
        self,
        screen,
        offset_x: int,
        offset_y: int,
        tile_size: int,
    ):
        frame = self.animation_manager.get_current_frame()

        remaining = self.remaining_time()
        if remaining < EXPLOSION_FADE_TIME:
            # cópia: o frame em cache é compartilhado com as outras explosões
            frame = frame.copy()
            frame.set_alpha(int(255 * max(remaining, 0) / EXPLOSION_FADE_TIME))

        for grid_x, grid_y in self.affected_tiles:
            screen.blit(frame, (grid_x * tile_size + offset_x, grid_y * tile_size + offset_y))
