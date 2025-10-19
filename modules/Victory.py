import os
import pygame
from typing import Tuple

from config.const import (
    PATH_BACKGROUNDS,
    PATH_CHARACTER,
    PATH_SOUNDS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    VICTORY_SCREEN_TIME,
    VICTORY_ANIMATION_SPEED,
    TICK_VALUE
)

class Victory:
    def __init__(self, players_count: int):
        self.players_count = players_count
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT
        self.can_skip = False
        self.start_time = 0
        self.animation_frame = 1
        self.last_animation_time = 0
        
        # Carregar recursos
        self.background = None
        self.victory_music = None
        self.player_animations = []
        self.fonts = {}
        
        self.load_resources()
        self.setup_fonts()
    
    def load_resources(self):
        try:
            self.victory_music = pygame.mixer.Sound(os.path.join(PATH_SOUNDS, 'win.wav'))
        except Exception as e:
            print(f"[ERROR] Erro ao carregar música de vitória: {e}")
        
        try:
            self.background = pygame.image.load(os.path.join(PATH_BACKGROUNDS, 'win-background.png')).convert()
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except Exception as e:
            print(f"[ERROR] Erro ao carregar background de vitória: {e}")
            # Fallback
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill("#000000")
        
        self.load_player_animations()
    
    def load_player_animations(self):
        for player_number in range(self.players_count):
            try:
                anim_frames = []
                for frame_count in range(1, 3):  # up to but nor including
                    frame_path = os.path.join(PATH_CHARACTER, f'{player_number+1}_win-front_{frame_count}.png')
                    frame = pygame.image.load(frame_path).convert_alpha()
                    if frame.get_size() != (100, 100):
                        frame = pygame.transform.scale(frame, (100, 100))
                    anim_frames.append(frame)
                self.player_animations.append(anim_frames)
            except Exception as e:
                print(f"[ERROR] Erro ao carregar animação do player {player_number+1}: {e}")
                self.create_fallback_animation(player_number)
    
    def create_fallback_animation(self, player_index: int):
        colors = ["#FF0000", "#00FF00"]  
        frames = []
        for j in range(4):
            surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            color = colors[player_index]
            
            radius = 30 + (j * 5)
            pygame.draw.circle(surf, color, (50, 50), radius)
            pygame.draw.circle(surf, "#FFFFFF", (50, 50), radius, 3)
            
            frames.append(surf)
        self.player_animations.append(frames)
    
    def setup_fonts(self):
        try:
            self.fonts = {
                'large': pygame.font.Font(None, 72),
                'medium': pygame.font.Font(None, 36),
                'small': pygame.font.Font(None, 24)
            }
        except:
            self.fonts = {
                'large': pygame.font.SysFont('Arial', 72),
                'medium': pygame.font.SysFont('Arial', 36),
                'small': pygame.font.SysFont('Arial', 24)
            }
    
    def update(self, current_time: int):
        if not self.can_skip and current_time - self.start_time > VICTORY_SCREEN_TIME:
            self.can_skip = True
        
        if current_time - self.last_animation_time > VICTORY_ANIMATION_SPEED:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.last_animation_time = current_time
    
    def render(self, screen: pygame.Surface, current_time: int):
        screen.blit(self.background, (0, 0))
        
        for i in range(self.players_count):
            if i < len(self.player_animations) and self.animation_frame < len(self.player_animations[i]):
                player_frame = self.player_animations[i][self.animation_frame]
                x_pos = self.screen_width // 2 - (self.players_count * 120) // 2 + i * 120
                screen.blit(player_frame, (x_pos, 250))
        
        if self.can_skip:
            continue_text = self.fonts['small'].render(
                "Press ENTER to go back to Main Menu", 
                True, "#AAAAAA"
            )
            continue_rect = continue_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
            screen.blit(continue_text, continue_rect)
        else:
            remaining = (VICTORY_SCREEN_TIME - (current_time - self.start_time)) // 1000 + 1
            countdown_text = self.fonts['small'].render(
                f"Continuing in {remaining}...", 
                True, "#AAAAAA"
            )
            countdown_rect = countdown_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
            screen.blit(countdown_text, countdown_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
            if event.key == pygame.K_RETURN and self.can_skip:
                return True
            if event.key and self.can_skip:  # Qualquer tecla após tempo mínimo
                return True
        return False
    
    def run(self, screen: pygame.Surface) -> bool:

        clock = pygame.time.Clock()
        
        if self.victory_music:
            self.victory_music.play(-1)  
        
        self.start_time = pygame.time.get_ticks()
        self.last_animation_time = self.start_time
        self.animation_frame = 1
        self.can_skip = False
        
        running = True
        should_return_to_menu = False
        
        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if self.handle_event(event):
                    should_return_to_menu = True
                    running = False
            
            self.update(current_time)
            
            self.render(screen, current_time)
            pygame.display.flip()
            
            clock.tick(TICK_VALUE)
        
        # Parar música
        if self.victory_music:
            self.victory_music.stop()
        
        return should_return_to_menu