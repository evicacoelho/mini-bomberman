from enum import Enum


class TileType(Enum):
    TERRAIN = 0     # can walk
    BLOCK = 1       # cant walk cant break
    BOX = 2         # cant walk can break
    DOOR = 3        # TODO
    KEYDOOR = 4     # TODO