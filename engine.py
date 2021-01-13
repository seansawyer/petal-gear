from typing import Set, Iterable

from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

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
        # Compute an initial field of view before first render
        self.update_fov()

    def handle_events(self, events: Iterable) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue
            action.perform(self, self.player)
            # Update field of view to reflect a changed position
            self.update_fov()

    def update_fov(self) -> None:
        """Recompute the field of view based on the player's position"""
        player_pos = self.player.x, self.player.y
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"], player_pos, radius=8
        )
        # Add any tiles the player has seen to her memory
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        for e in self.entities:
            # Only show entities in the player's field of view
            if self.game_map.visible[e.x, e.y]:
                console.print(e.x, e.y, e.char, fg=e.color)
        context.present(console, integer_scaling=True)
        console.clear()
