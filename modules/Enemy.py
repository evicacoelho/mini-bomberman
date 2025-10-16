import os
import random

import pygame

from config.const import ENEMY_MOVE_COOLDOWN, ENEMY_MOVE_DELAY, PATH_ENEMIES, PATH_SOUNDS
from modules.AnimationManager import AnimationManager
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
        self.last_direction = 'front'
        self.moving = False

        # animações
        self.animation_manager = AnimationManager()
        self.load_animations()

        # sons
        self.sounds = {}
        self.load_sounds()

    def load_animations(self):
        enemy_path = os.path.join(PATH_ENEMIES, "bat")
        
        # walk
        self.animation_manager.load_animation("walk_front", enemy_path, 3, "fly-front_{}.png")
        self.animation_manager.load_animation("walk_back", enemy_path, 3, "fly-back_{}.png")
        self.animation_manager.load_animation("walk_left", enemy_path, 3, "fly-persp-left_{}.png")
        self.animation_manager.load_animation("walk_right", enemy_path, 3, "fly-persp-right_{}.png")

        # die
        self.animation_manager.load_animation("death", enemy_path, 5, "death-front_{}.png")

    def load_sounds(self):
        try:
            self.sounds['walking'] = pygame.mixer.Sound(os.path.join(PATH_SOUNDS, 'enemy_walking.wav'))
            self.sounds['walking'].set_volume(0.1)
            self.sounds['death'] = pygame.mixer.Sound(os.path.join(PATH_SOUNDS, 'enemy_dies.wav'))
            pass
        except Exception as e:
            print(f"[ERROR] Erro ao carregar sons do inimigo: {e}")


    def update(self, game):
        current_time = pygame.time.get_ticks()
        
        self.move_cooldown -= 1
        if self.move_cooldown <= 0:
            self.random_move(game)
            self.move_cooldown = self.move_delay
            self.moving = True
        else:
            self.moving = False

        if self.moving:
            animation_name = f"walk_{self.last_direction}"
        else:
            animation_name = f"idle_{self.last_direction}"
            
        self.animation_manager.set_animation(animation_name)
        self.animation_manager.update(current_time)

    def random_move(self, game):
        directions = [
            (0, -1, "back"),   # up
            (0, 1, "front"),   # down  
            (-1, 0, "left"),   # left
            (1, 0, "right")    # right
        ]
        random.shuffle(directions)
        
        current_x, current_y = self.position
        
        for dx, dy, direction in directions:
            new_x, new_y = current_x + dx, current_y + dy
            if game.is_walkable(new_x, new_y):
                self.position = (new_x, new_y)
                self.last_direction = direction
                self.sounds['walking'].play()
                break

    def take_damage(self, damage: int = 1):
        result = super().take_damage(damage)
        if not self.alive:
            self.sounds['death'].play()
            pass
        return result

    def render(self, screen, offset_x: int, offset_y: int, tile_size: int):
        pixel_x = self.position[0] * tile_size + offset_x
        pixel_y = self.position[1] * tile_size + offset_y
        
        current_frame = self.animation_manager.get_current_frame()
        
        # Escala a imagem para o tamanho do tile se necessário
        if current_frame.get_size() != (tile_size, tile_size):
            current_frame = pygame.transform.scale(current_frame, (tile_size, tile_size))
        
        screen.blit(current_frame, (pixel_x, pixel_y))