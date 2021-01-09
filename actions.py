from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action(ABC):

    @abstractmethod
    def perform(self, engine: Engine, Entity: Entity):
        pass


class QuitAction(Action):

    def perform(self, _engine: Engine, _entity: Entity):
        raise SystemExit()


class MoveAction(Action):

    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        if engine.game_map.tiles["walkable"][dest_x, dest_y]:
            entity.move(self.dx, self.dy)

