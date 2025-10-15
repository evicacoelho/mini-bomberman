from abc import ABC, abstractmethod
from typing import Tuple

class Entity(ABC):
    def __init__(
        self,
        name: str,
        position: Tuple[int, int]
    ):
        super().__init__()
        self.name = name
        self.position = position

    @abstractmethod
    def move_up(self, speed: int):
        pass

    @abstractmethod
    def move_down(self, speed: int):
        pass
    
    @abstractmethod
    def move_left(self, speed: int):
        pass

    @abstractmethod
    def move_right(self, speed: int):
        pass

