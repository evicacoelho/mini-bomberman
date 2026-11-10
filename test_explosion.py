from modules.Explosion import calculate_affected_tiles
from modules.TileType import TileType as T

# 5x5: centro (2,2); parede logo acima, caixa logo à esquerda
LAYOUT = [
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 2, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]

def tile_at(x, y):
    if 0 <= y < len(LAYOUT) and 0 <= x < len(LAYOUT[0]):
        return T(LAYOUT[y][x])
    return T.BLOCK

tiles = set(calculate_affected_tiles((2, 2), 2, tile_at))
assert (2, 1) not in tiles and (2, 0) not in tiles, "parede bloqueia"
assert (1, 2) in tiles and (0, 2) not in tiles, "caixa é atingida e para a explosão"
assert {(3, 2), (4, 2)} <= tiles, "espaço aberto: alcance completo"
assert (2, 3) in tiles and (2, 4) not in tiles, "para antes da borda"
print("ok")
