from typing import List, Tuple

import pygame
from config.const import BOMB_COUNT, BOMB_RANGE, CONTROLS, ENTITY_HEALTH, ENTITY_SPEED, PATH_CHARACTER, PLAYER_MOVE_COOLDOWN, PLAYER_MOVE_DELAY
from modules.AnimationManager import AnimationManager
from modules.Bomb import Bomb
from modules.Entity import Entity, EntityType


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
        self.lives = ENTITY_HEALTH[self.name]
        self.bomb_count = BOMB_COUNT
        self.bomb_range = BOMB_RANGE
        self.placed_bombs: List[Bomb] = []
        self.last_direction = 'front'
        self.moving = False

        # controles
        self.controls = CONTROLS[self.name]

        # movimentação
        self.move_delay = PLAYER_MOVE_DELAY
        self.move_cooldown = PLAYER_MOVE_COOLDOWN

        # animações
        self.animation_manager = AnimationManager()
        self.load_animations()

        # sons
        self.sounds = {}

    def load_animations(self):
        # idle
        self.animation_manager.load_animation("idle_front", PATH_CHARACTER, 4, "idle-front_{}.png")
        self.animation_manager.load_animation("idle_back", PATH_CHARACTER, 4, "idle-back_{}.png")
        self.animation_manager.load_animation("idle_left", PATH_CHARACTER, 4, "idle-left_{}.png")
        self.animation_manager.load_animation("idle_right", PATH_CHARACTER, 4, "idle-right_{}.png")
        
        # walk
        self.animation_manager.load_animation("walk_front", PATH_CHARACTER, 4, "walk-front_{}.png")
        self.animation_manager.load_animation("walk_back", PATH_CHARACTER, 4, "walk-back_{}.png")
        self.animation_manager.load_animation("walk_left", PATH_CHARACTER, 4, "walk-left_{}.png")
        self.animation_manager.load_animation("walk_right", PATH_CHARACTER, 4, "walk-right_{}.png")
        
        # death
        self.animation_manager.load_animation("death", PATH_CHARACTER, 2, "death-front_{}.png")

        # win
        self.animation_manager.load_animation("win", PATH_CHARACTER, 2, "win-front_{}.png")

    def update(
        self,
        game
    ):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        grid_x, grid_y = self.position

        new_x, new_y = grid_x, grid_y
        self.moving = False
        moved = False

        # movement
        if current_time > self.move_cooldown:
            moved = False
            new_x, new_y = self.position

            if keys[self.controls['up']]:
                new_y -= self.speed
                self.last_direction = "back"
                self.moving = True
                moved = True
            elif keys[self.controls['down']]:
                new_y += self.speed
                self.last_direction = "front"
                self.moving = True
                moved = True
            elif keys[self.controls['left']]:
                new_x -= self.speed
                self.last_direction = "left"
                self.moving = True
                moved = True
            elif keys[self.controls['right']]:
                new_x += self.speed
                self.last_direction = "right"
                self.moving = True
                moved = True

        if moved and game.is_walkable(new_x, new_y):
            self.position = (new_x, new_y)
            self.move_cooldown = current_time + self.move_delay
        elif moved:
            self.moving = True
            self.move_cooldown = current_time + self.move_delay // 2

        if keys[self.controls['bomb']] and len(self.placed_bombs) < self.bomb_count:
            self.place_bomb(game)

        if self.moving:
            animation_name = f"walk_{self.last_direction}"
        else:
            animation_name = f"idle_{self.last_direction}"

        self.animation_manager.set_animation(animation_name)
        self.animation_manager.update(current_time)


    def place_bomb(
        self,
        game
    ):
        from modules.EntityFactory import EntityFactory
        bomb = EntityFactory.create_bomb(self.position, self.bomb_range, self)
        
        self.placed_bombs.append(bomb)
        game.entity_manager.add_entity(bomb)

        if not bomb.alive:
            self.placed_bombs.remove(bomb)
        
    def lose_life(self) -> bool:
        self.lives -= 1
        if self.lives <= 0:
            self.alive = False
        
        return self.lives <= 0
        

    def render(self, screen, offset_x: int, offset_y: int, tile_size: int):
        pixel_x = self.position[0] * tile_size + offset_x
        pixel_y = self.position[1] * tile_size + offset_y
        
        current_frame = self.animation_manager.get_current_frame()
        
        # Escala a imagem para o tamanho do tile se necessário
        if current_frame.get_size() != (tile_size, tile_size):
            current_frame = pygame.transform.scale(current_frame, (tile_size, tile_size))
        
        screen.blit(current_frame, (pixel_x, pixel_y))
