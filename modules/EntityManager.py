from typing import List

from modules.Entity import Entity, EntityType
from modules.Game import Game, TileType
from modules.Player import Player

class EntityManager:
    def __init__(self):
        self.entities: List[Entity]
        self.players: List[Player]
    
    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        if entity.entity_type == EntityType.PLAYER:
            self.players.append(entity)

    def update_entities(self, game: Game):
        for entity in self.entities[:]:
            entity.update(game)

            if not entity.alive:
                self.entities.remove(entity)
                if entity.entity_type == EntityType.PLAYER:
                    self.players.remove(entity)

        self.check_collisions(game)

    def check_collisions(self, game: Game):
        for player in self.players:
            for entity in self.entities:
                if (
                    entity.entity_type == EntityType.ENEMY and
                    entity.get_grid_position() == player.get_grid_position()
                ):
                    player.lose_life()

                elif entity.entity_type == EntityType.EXPLOSION:
                    explosion = entity
                    if player.get_grid_position() in explosion.affected_tiles:
                        player.lose_life()

                    for other_entity in self.entities:
                        if (
                            other_entity.entity_type == EntityType.ENEMY and
                            other_entity.get_grid_position() in explosion.affected_tiles
                        ):
                            other_entity.take_damage()

                    for tile in explosion.affected_tiles:
                        grid_x, grid_y = tile
                        if game.get_tile_at_position(grid_x, grid_y) == TileType.BOX:
                            game.destroy_box(grid_x, grid_y)
                        
    # getters/setters
    def get_players(self) -> List[Player]:
        return self.players
    
    def get_entities_by_type(self, entity_type: EntityType) -> List[Entity]:
        return [entity for entity in self.entities if entity.entity_type == entity_type]
    
    def clear_all_entities(self):
        self.entities.clear()
        self.players.clear()