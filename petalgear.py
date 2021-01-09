import tcod
import time

import sdl2
import sdl2.ext

from actions import Action, MoveAction, QuitAction
from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


def main():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_GAMECONTROLLER)
    tileset_path = "dejavu10x10_gs_tc.png"
    tileset = tcod.tileset.load_tilesheet(
        tileset_path, 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    player = Entity(
        int(screen_width / 2),
        int(screen_height / 2),
        "@",
        (255, 255, 255),
    )
    npc = Entity(
        player.x - 5,
        int(screen_height / 2),
        "@",
        (255, 255, 0),
    )
    entities = {npc, player}
    game_map = GameMap(map_width, map_height)
    engine = Engine(entities, player, game_map)
    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="PETAL GEAR",
            vsync=True
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.print(player.x, player.y, "@", fg=player.color)
            engine.render(root_console, context)
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == '__main__':
    main()
