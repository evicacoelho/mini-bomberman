from typing import Tuple
from abc import ABC, abstractmethod

from modules.EntityType import EntityType

class Entity(ABC):
    def __init__(
        self,
        name: str,
        position: Tuple[int, int],
        entity_type: EntityType,
        speed: int = 1,
    ):
        super().__init__()
        self.name = name
        self.entity_type = entity_type
        self.position = position
        self.previous_position = position
        self.speed = speed
        self.hp = 1
        self.alive = True

    @abstractmethod
    def update(self, game):
        pass

    def render(
        self,
        screen,
        offset_x: int,
        offset_y: int,
        tile_size: int,
    ):
        # frames já vêm no tamanho do tile (AnimationManager)
        screen.blit(
            self.animation_manager.get_current_frame(),
            (self.position[0] * tile_size + offset_x, self.position[1] * tile_size + offset_y),
        )

    def take_damage(
        self,
        damage: int = 1,
    ) -> bool:
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            print(f"[INFO] {self.name} foi destruído")
        return self.alive
    
    def get_grid_position(self) -> Tuple[int, int]:
        return self.position
    
    def set_grid_position(
        self,
        grid_x: int,
        grid_y: int,
    ) -> Tuple[int, int]:
        self.position = (grid_x, grid_y)
