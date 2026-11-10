import os
import sys
import pygame
import random

from typing import List, Tuple

from config.const import (
    ENEMY_MAX_NUMBER,
    ENEMY_MIN_NUMBER,
    ENEMY_SPAWN_MIN_DISTANCE,
    GRID_LENGTH,
    GRID_HEIGHT,
    OFFSET_X,
    OFFSET_Y,
    PATH_ITEMS,
    PATH_SOUNDS,
    PATH_TERRAIN,
    PLAYER_SPAWN_COORDS,
    STAGE_SCREEN_TIME,
    TICK_VALUE,
    TILE_SIZE
)
from config.levels import LEVELS
from modules.TileType import TileType
from modules.Entity import EntityType
from modules.assets import load_image, load_sound
from modules.Enemy import Enemy
from modules.Player import Player
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
        self.sounds = {}
        self.load_sounds()

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


    def load_sounds(self):
        try:
            self.sounds['background'] = load_sound(os.path.join(PATH_SOUNDS, 'game.mp3'))
            self.sounds['stage'] = load_sound(os.path.join(PATH_SOUNDS, 'stage_intro.wav'))
            pass
        except Exception as e:
            print(f"[ERROR] Erro ao carregar sons do inimigo: {e}")


    def load_tile_images(self):
        try:
            self.tile_variants = {
                TileType.TERRAIN: [],
                TileType.BLOCK: [],
                TileType.BOX: []
            }
            
            for i in range(1, LEVELS[self.level]['terrain']['variations'] + 1):
                img = load_image(os.path.join(PATH_TERRAIN, f'{LEVELS[self.level]['terrain']['asset_name']}_{i}.png'))
                self.tile_variants[TileType.TERRAIN].append(img)
            
            for i in range(1, LEVELS[self.level]['block']['variations'] + 1):
                img = load_image(os.path.join(PATH_TERRAIN, f'{LEVELS[self.level]['block']['asset_name']}_{i}.png'))
                self.tile_variants[TileType.BLOCK].append(img)
            
            for i in range(1, 10):
                img = load_image(os.path.join(PATH_ITEMS, f'box_{i}.png'))
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

    def show_stage_screen(self, screen: pygame.Surface):
        """Retorna True para jogar, 'menu' no ESC, None ao fechar a janela."""
        clock = pygame.time.Clock()
        display_time = STAGE_SCREEN_TIME  
        start_time = pygame.time.get_ticks()
        
        try:
            font_large = pygame.font.Font(None, 72)
            font_small = pygame.font.Font(None, 36)
        except:
            font_large = pygame.font.SysFont('Arial', 72)
            font_small = pygame.font.SysFont('Arial', 36)

        self.sounds['stage'].play()
        while pygame.time.get_ticks() - start_time < display_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'menu'
                    if event.key:
                        return True
            
            # Preenche a tela com preto
            screen.fill("#000000")
            
            # Renderiza "STAGE"
            stage_text = font_large.render(f"STAGE: {self.level}", True, "#FFFF00")
            stage_rect = stage_text.get_rect(center=(self.width // 2 + OFFSET_X, self.height // 2 + OFFSET_Y - 50))
            screen.blit(stage_text, stage_rect)
            
            # Renderiza o número da fase
            level_text = font_small.render("Kill All Your Enemies!", True, "#FFFFFF")
            level_rect = level_text.get_rect(center=(self.width // 2 + OFFSET_X, self.height // 2 + OFFSET_Y + 20))
            screen.blit(level_text, level_rect)
            
            pygame.display.flip()
            clock.tick(TICK_VALUE)
        
        return True
            
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
        if tile_type != TileType.TERRAIN:
            return False
        return not any(
            entity.entity_type == EntityType.BOMB and entity.position == (grid_x, grid_y)
            for entity in self.entity_manager.entities
        )
    
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

        for number in range(1, self.players_count + 1):
            name = f'player{number}'
            self.entity_manager.add_entity(
                Player(name, position=PLAYER_SPAWN_COORDS[name], player_number=number)
            )

        # random enemies
        enemy_count = min(self.level + ENEMY_MIN_NUMBER, ENEMY_MAX_NUMBER)
        player_spawns = [player.position for player in self.entity_manager.get_players()]
        for i in range(enemy_count):
            while True:
                x = random.randint(1, self.grid_length - 2)
                y = random.randint(1, self.grid_height - 2)
                too_close = any(
                    abs(x - px) + abs(y - py) < ENEMY_SPAWN_MIN_DISTANCE
                    for px, py in player_spawns
                )
                if self.is_walkable(x, y) and not too_close:
                    enemy = Enemy(f"Enemy{i+1}", (x, y))
                    self.entity_manager.add_entity(enemy)
                    break

    def render_hud(self, screen: pygame.Surface, font: pygame.font.Font):
        # vidas sobre a fileira de blocos do topo
        text = "   ".join(
            f"P{player.player_number}: {max(player.lives, 0)} vidas"
            for player in self.entity_manager.get_players()
        )
        screen.blit(font.render(text, True, "#FFFFFF"), (OFFSET_X + 8, OFFSET_Y + 8))

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

    def run(self, screen: pygame.Surface) -> bool:
        if self.level in LEVELS:
            self.set_level_layout(LEVELS[self.level]['layout'])

        self.initialize_level_entities()

        stage_result = self.show_stage_screen(screen)
        if stage_result is not True:
            return stage_result

        clock = pygame.time.Clock()
        hud_font = pygame.font.Font(None, 24)
        run = True
        result = None

        self.sounds['background'].play(-1)
        try:
            while run and result is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return None

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            return 'menu'

                self.entity_manager.update_entities(self)
                result = self.check_game_conditions()

                screen.fill("#FFFFFF")
                self.render(screen)
                self.entity_manager.render_entities(screen, OFFSET_X, OFFSET_Y, self.tile_size)
                self.render_hud(screen, hud_font)
                pygame.display.flip()
                clock.tick(TICK_VALUE)
                
        finally:
            self.sounds['background'].stop()
            pygame.mixer.stop()

        return result