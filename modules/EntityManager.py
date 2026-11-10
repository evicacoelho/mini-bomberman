from typing import List

from modules.Entity import Entity, EntityType
from modules.TileType import TileType
from modules.Player import Player

class EntityManager:
    def __init__(self):
        self.entities: List[Entity] = []
        self.players: List[Player] = []
    
    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        if entity.entity_type == EntityType.PLAYER:
            self.players.append(entity)

    def update_entities(self, game):
        for entity in self.entities[:]:
            entity.previous_position = entity.position
            entity.update(game)

            if not entity.alive:
                self.entities.remove(entity)
                if entity.entity_type == EntityType.PLAYER:
                    self.players.remove(entity)

        self.check_collisions(game)

    def check_collisions(self, game):
        for player in self.players:
            for entity in self.entities:
                if entity.entity_type == EntityType.ENEMY and (
                    entity.get_grid_position() == player.get_grid_position() or
                    # trocaram de tile no mesmo frame: passaram um pelo outro
                    (entity.position == player.previous_position and
                     entity.previous_position == player.position)
                ):
                    player.lose_life()

                elif (
                    entity.entity_type == EntityType.EXPLOSION and
                    player.get_grid_position() in entity.affected_tiles
                ):
                    player.lose_life()

        # explosões afetam inimigos e caixas uma vez, com ou sem jogadores vivos
        for explosion in self.get_entities_by_type(EntityType.EXPLOSION):
            for enemy in self.get_entities_by_type(EntityType.ENEMY):
                if enemy.alive and enemy.get_grid_position() in explosion.affected_tiles:
                    enemy.take_damage()

            for grid_x, grid_y in explosion.affected_tiles:
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

    def render_entities(
        self, 
        screen, 
        offset_x: int, 
        offset_y: int, 
        tile_size: int
    ):
        for entity in self.entities:
            entity.render(screen, offset_x, offset_y, tile_size)