from typing import Set, Iterable

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    """Core game state and logic"""

    def __init__(self, entities: Set[Entity], player: Entity, game_map: GameMap):
        self.entities = entities
        self.player = player
        self.game_map = game_map
        self.event_handler = EventHandler()

    def handle_events(self, events: Iterable) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue
            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        for e in self.entities:
            console.print(e.x, e.y, e.char, fg=e.color)
        context.present(console, integer_scaling=True)
        console.clear()
