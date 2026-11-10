from typing import Tuple

from config.const import PLAYER_SPAWN_COORDS
from modules.Bomb import Bomb
from modules.Enemy import Enemy
from modules.Player import Player
from modules.Explosion import Explosion


class EntityFactory:
    @staticmethod
    def create_player(
        name: str,
    ) -> Player:
        match name:
            case 'player1':
                return Player(name, player_number=1, position=PLAYER_SPAWN_COORDS[name])
            case 'player2':
                return Player(name, player_number=2, position=PLAYER_SPAWN_COORDS[name])
            
    @staticmethod
    def create_enemy(
        name: str,
        position: Tuple[int, int],
    ) -> Enemy:
        return Enemy(name, position)
            
    @staticmethod
    def create_bomb(
        position: Tuple[int, int],
        explosion_range: int,
        owner
    ) -> Bomb:
        return Bomb(position, explosion_range, owner)
        
    @staticmethod
    def create_explosion(
        position: Tuple[int, int],
        explosion_range: int,
        owner,
        game,
    ) -> Explosion:
        return Explosion(position, explosion_range, owner, game)