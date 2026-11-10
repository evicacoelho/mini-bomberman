from functools import cache

import pygame


@cache
def load_image(path: str, size=None) -> pygame.Surface:
    """Carrega (e redimensiona) cada imagem uma única vez. Superfícies são
    compartilhadas: use .copy() antes de alterá-las (ex.: set_alpha)."""
    image = pygame.image.load(path).convert_alpha()
    if size and image.get_size() != size:
        image = pygame.transform.scale(image, size)
    return image


@cache
def load_sound(path: str) -> pygame.mixer.Sound:
    return pygame.mixer.Sound(path)
