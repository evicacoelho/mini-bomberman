from typing import List, Self, Tuple
from config.const import EXPLOSION_DURATION
from modules.Entity import Entity, EntityType
from modules.Game import Game


class Explosion(Entity):
    def __init__(
        self,  
        position: int, 
        explosion_range: int, 
        owner,
    ):
        super().__init__("Explosion", position, EntityType.EXPLOSION)
        self.explosion_range = explosion_range
        self.owner = owner
        self.duration = EXPLOSION_DURATION
        self.affected_tiles = self.calculate_affected_tiles()

    def calculate_affected_tiles(self) -> List[Tuple[int, int]]:
        center_x, center_y = self.position

        affected_tiles = [(center_x, center_y)]

        directions = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]

        for dx, dy in directions:
            for i in range(1, self.explosion_range +1):
                tile = (center_x + dx * i, center_y + dx * i)
                affected_tiles.append(tile)

        return affected_tiles
    
    def update(self, game: Game):
        self.duration -= 1
        if self.duration <= 0:
            self.alive = False