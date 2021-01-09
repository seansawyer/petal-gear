from typing import Tuple


class Entity:
    """
    Represents anything that may appear in the game world: players, enemies, items, et.
    """

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
