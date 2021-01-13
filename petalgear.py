import tcod
import time

import numpy as np
import sdl2
import sdl2.ext

from actions import Action, MoveAction, QuitAction
from engine import Engine
from entity import Entity
from procgen import generate_dungeon
from input_handlers import EventHandler


def main():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_GAMECONTROLLER)
    # a 32px tileset with only the "@" filled in currently
    tileset_path = "tileset.png"
    tileset = tcod.tileset.load_tilesheet(
        tileset_path, 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    screen_width = 32
    screen_height = 24
    map_width = 32
    map_height = 20
    game_map = generate_dungeon(
        max_rooms=6,
        room_min_size=4,
        room_max_size=10,
        map_width=map_width,
        map_height=map_height,
    )
    # filter for walkable tiles and place the player and NPC there
    walkable_positions = np.where(game_map.tiles["walkable"])
    player_x = walkable_positions[0][0]
    player_y = walkable_positions[1][0]
    npc_x = walkable_positions[0][1]
    npc_y = walkable_positions[1][1]
    player = Entity(
        player_x,
        player_y,
        "@",
        (255, 255, 255),
    )
    npc = Entity(
        npc_x,
        npc_y,
        "@",
        (255, 255, 0),
    )
    entities = {npc, player}
    engine = Engine(entities, player, game_map)
    sdl_window_flags = tcod.context.SDL_WINDOW_MAXIMIZED
    with tcod.context.new(
            columns=screen_width,
            rows=screen_height,
            tileset=tileset,
            title="PETAL GEAR",
            vsync=True,
            sdl_window_flags=sdl_window_flags
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(player.x, player.y, "@", fg=player.color)
            engine.render(root_console, context)
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == '__main__':
    main()
