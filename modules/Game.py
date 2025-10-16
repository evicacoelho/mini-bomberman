import os
import sys
import pygame
import random

from typing import List, Tuple

from config.const import (
    ENEMY_MAX_NUMBER,
    ENEMY_MIN_NUMBER,
    GRID_LENGTH,
    GRID_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    PATH_ITEMS,
    PATH_SOUNDS,
    PATH_TERRAIN,
    TICK_VALUE,
    TILE_SIZE
)
from config.levels import LEVELS
from modules.TileType import TileType
from modules.Entity import EntityType
from modules.EntityFactory import EntityFactory
from modules.EntityManager import EntityManager

class Game:
    def __init__(
        self,
        level: int,
        players_count: int = 1
    ):
        self.level = level
        self.players_count = players_count
        self.tile_size = TILE_SIZE
        self.grid_height = GRID_HEIGHT
        self.grid_length = GRID_LENGTH
        self.height = self.tile_size * self.grid_height
        self.width = self.tile_size * self.grid_length
        self.tiles: List[List[TileType]] = []
        self.tile_images: dict = {}

        # inicializador do grid
        self._initialize_grid()
        self.load_tile_images()

        # entidades
        self.entity_manager = EntityManager()

        # seed de nívels
        random.seed(level * 42)

        # background song
        pygame.mixer.music.load(os.path.join(PATH_SOUNDS, 'game.mp3'))
        pygame.mixer.music.play(-1)

    def _initialize_grid(self):
        self.tiles = []

        for row in range(self.grid_height):
            self.tiles.append([])
            for col in range(self.grid_length):
                if (row == 0 or row == self.grid_height - 1 or col == 0 or col == self.grid_length - 1):
                    self.tiles[row].append(TileType.BLOCK)
                else: self.tiles[row].append(TileType.TERRAIN)

    def _create_fallback_tiles(self):
        self.tile_images[TileType.TERRAIN] = pygame.Surface((self.tile_size, self.tile_size))
        self.tile_images[TileType.TERRAIN].fill("#64C864")

        self.tile_images[TileType.BLOCK] = pygame.Surface((self.tile_size, self.tile_size))
        self.tile_images[TileType.BLOCK].fill("#646464")

        self.tile_images[TileType.BOX] = pygame.Surface((self.tile_size, self.tile_size))
        self.tile_images[TileType.BOX].fill("#966432")


    def load_tile_images(self):
        try:
            self.tile_variants = {
                TileType.TERRAIN: [],
                TileType.BLOCK: [],
                TileType.BOX: []
            }
            
            for i in range(1, 4):
                img = pygame.image.load(os.path.join(PATH_TERRAIN, f'grass_{i}.png')).convert_alpha()
                self.tile_variants[TileType.TERRAIN].append(img)
            
            for i in range(1, 5):
                img = pygame.image.load(os.path.join(PATH_TERRAIN, f'wood_{i}.png')).convert_alpha()
                self.tile_variants[TileType.BLOCK].append(img)
            
            for i in range(1, 10):
                img = pygame.image.load(os.path.join(PATH_ITEMS, f'box_{i}.png')).convert_alpha()
                self.tile_variants[TileType.BOX].append(img)
            
            self.variants_map = []
            for row in range(self.grid_height):
                self.variants_map.append([])
                for col in range(self.grid_length):
                    tile_type = self.tiles[row][col]
                    variants = self.tile_variants.get(tile_type, [])
                    if variants:
                        variant_index = random.randint(0, len(variants) - 1)
                        self.variants_map[row].append(variant_index)
                    else:
                        self.variants_map[row].append(0)
                        
        except Exception as e:
            print(f"[ERROR] Erro ao carregar imagens: {e}")
            self._create_fallback_tiles()
            
    def set_level_layout(
        self,
        level_data: List[List[int]]
    ):
        for row in range(min(len(level_data), self.grid_height)):
            for col in range(min(len(level_data[row]), self.grid_length)):
                tile_type = TileType(level_data[row][col])
                self.tiles[row][col] = tile_type

    def get_tile_at_position(
        self,
        grid_x: int,
        grid_y: int,
    ) -> TileType:
        if 0 <= grid_x < self.grid_length and 0 <= grid_y < self.grid_height:
            return self.tiles[grid_y][grid_x]
        return TileType.BLOCK
    
    def is_walkable(
        self,
        grid_x: int,
        grid_y: int,
    ) -> bool:
        tile_type = self.get_tile_at_position(grid_x=grid_x, grid_y=grid_y)
        return tile_type == TileType.TERRAIN
    
    def destroy_box(self, grid_x: int, grid_y: int) -> bool:
        if (0 <= grid_x < self.grid_length and 0 <= grid_y < self.grid_height and
            self.tiles[grid_y][grid_x] == TileType.BOX):
            self.tiles[grid_y][grid_x] = TileType.TERRAIN
            return True
        return False
    
    def grid_to_pixel(
        self,
        grid_x: int,
        grid_y: int,
    ) -> Tuple[int, int]:
        return (grid_x * self.tile_size, grid_y * self.tile_size)
    
    def pixel_to_grid(
        self,
        pixel_x: int,
        pixel_y: int,
        offset_x: int = OFFSET_X,
        offset_y: int = OFFSET_Y,
    ) -> Tuple[int, int]:
        return ((pixel_x - offset_x) // self.tile_size, (pixel_y - offset_y) // self.tile_size)
    
    def render(
        self, 
        screen: pygame.Surface, 
        offset_x: int = OFFSET_X, 
        offset_y: int = OFFSET_Y
    ):
        for row in range(self.grid_height):
            for col in range(self.grid_length):
                tile_type = self.tiles[row][col]
                
                # Renderiza terreno
                terrain_variants = self.tile_variants.get(TileType.TERRAIN, [])
                if terrain_variants:
                    variant_index = self.variants_map[row][col] % len(terrain_variants)
                    screen.blit(
                        terrain_variants[variant_index],
                        (col * self.tile_size + offset_x, row * self.tile_size + offset_y)
                    )
                
                # Renderiza tile por cima se não for terreno
                if tile_type != TileType.TERRAIN:
                    tile_variants = self.tile_variants.get(tile_type, [])
                    if tile_variants:
                        variant_index = self.variants_map[row][col] % len(tile_variants)
                        screen.blit(
                            tile_variants[variant_index],
                            (col * self.tile_size + offset_x, row * self.tile_size + offset_y)
                        )
    
    def initialize_level_entities(self):
        self.entity_manager.clear_all_entities()

        player1 = EntityFactory.create_player('player1')
        self.entity_manager.add_entity(player1)

        if self.players_count == 2:
            player2 = EntityFactory.create_player('player2')
            self.entity_manager.add_entity(player2)

        # random enemies
        enemy_count = min(self.level + ENEMY_MIN_NUMBER, ENEMY_MAX_NUMBER)
        for i in range(enemy_count):
            while True:
                x = random.randint(1, self.grid_length - 2)
                y = random.randint(1, self.grid_height - 2)
                if self.is_walkable(x, y):
                    enemy = EntityFactory.create_enemy(f"Enemy{i+1}", (x, y))
                    self.entity_manager.add_entity(enemy)
                    break

    def check_game_conditions(self) -> bool:
        players = self.entity_manager.get_players()
        enemies = self.entity_manager.get_entities_by_type(entity_type=EntityType.ENEMY)

        # defeat
        if len(players) == 0:
            return False
        
        # victory
        if len(enemies) == 0:
            return True
        
        return None

    def run(
        self,
        screen: pygame.Surface
    ) -> bool:
        if self.level in LEVELS:
            self.set_level_layout(LEVELS[self.level])

        self.initialize_level_entities()

        clock = pygame.time.Clock()
        run = True
        result = None

        while run and result is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            self.entity_manager.update_entities(self)

            result = self.check_game_conditions()

            screen.fill("#FFFFFF")
            self.render(screen)

            self.entity_manager.render_entities(screen, OFFSET_X, OFFSET_Y, self.tile_size)

            pygame.display.flip()
            clock.tick(TICK_VALUE) 

        if result is None:
            result = False

        pygame.mixer.music.stop()
        return result