import os
import pygame
from typing import Dict

from config.const import ANIMATION_SPEED

class AnimationManager:
    def __init__(self):
        self.animations: Dict[str, Dict] = {}
        self.current_animation: str = ""
        self.current_frame: int = 0
        self.animation_speed: int = ANIMATION_SPEED
        self.last_update: int = 0

    def load_animation(
        self,
        animation_name: str,
        base_path: str,
        frame_count: int,
        file_pattern: str = "{}"
    ):
        frames = []
        for i in range(1, frame_count + 1):
            try:
                frame_path = os.path.join(base_path, file_pattern.format(i))
                image = pygame.image.load(frame_path).convert_alpha()
                frames.append(image)
            except Exception as e:
                print(f"[ERROR] Erro ao carregar frame {i} para {animation_name}: {e}")
                fallback_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
                color = "#FF0000" if "enemy" in animation_name else "#00FF00"
                pygame.draw.rect(fallback_surface, color, (0, 0, 32, 32))
                frames.append(fallback_surface)
        
        self.animations[animation_name] = {
            'frames': frames,
            'frame_count': len(frames)
        }

        if not self.current_animation:
            self.current_animation = animation_name

    def set_animation(
        self,
        animation_name: str,
    ):
        if animation_name in self.animations and self.current_animation != animation_name:
            self.current_animation = animation_name
            self.current_frame = 0

    def update(self, current_time: int):
        if (self.current_animation and 
            self.current_animation in self.animations and
            (current_time - self.last_update) > self.animation_speed):
            
            animation_data = self.animations[self.current_animation]
            frame_count = animation_data['frame_count']
            
            if frame_count > 0:
                self.current_frame = (self.current_frame + 1) % frame_count
                self.last_update = current_time

    def get_current_frame(self) -> pygame.Surface:
        if (self.current_animation and 
            self.current_animation in self.animations):
            
            # CORREÇÃO: Acessar corretamente os frames
            animation_data = self.animations[self.current_animation]
            frames = animation_data['frames']
            
            if frames and 0 <= self.current_frame < len(frames):
                return frames[self.current_frame]
        
        # Fallback - surface vermelha para debug
        fallback = pygame.Surface((32, 32), pygame.SRCALPHA)
        fallback.fill("#FF0000")
        return fallback
