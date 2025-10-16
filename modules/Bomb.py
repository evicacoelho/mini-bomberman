from typing import Self, Tuple
from config.const import EXPLOSION_TIMER
from modules.Entity import Entity, EntityType
from modules.Game import Game


class Bomb(Entity):
    def __init__(
        self, 
        position: Tuple[int, int],
        explosion_range: int,
        owner,
    ):
        super().__init__("Bomb", position, EntityType.BOMB)
        self.explosion_range = explosion_range
        self.owner = owner
        self.timer = EXPLOSION_TIMER
        self.exploded = False

    def update(
        self, 
        game: Game
    ):
        self.timer -= 1
        if self.timer <= 0:
            self.explode(game)

    def explode(
        self,
        game: Game,
    ):
        self.exploded = True
        self.alive = False

        from modules.EntityFactory import EntityFactory
        explosion = EntityFactory.create_explosion(
            self.position,
            self.explosion_range,
            self.owner
        )

        game.entity_manager.add_entity(explosion)