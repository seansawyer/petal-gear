from __future__ import annotations
import random
from typing import Iterator, Tuple

import tcod

from game_map import GameMap
import tile_types


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """Return the coordinates of the approximate center of the room"""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the indices of the room's inner tiles as a two-dimensional slice"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return `True` if this room overlaps the other room"""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
) -> GameMap:
    """Generate a dungeon by carving floors out of a map full of walls"""
    dungeon = GameMap(map_width, map_height)
    rooms: List[RectangularRoom] = []
    while len(rooms) < max_rooms:
        # size and place the room
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)
        room = RectangularRoom(x, y, room_width, room_height)
        # avoid creating overlapping rooms
        if any(room.intersects(other_room) for other_room in rooms):
            continue
        # clear out the room's inner area
        dungeon.tiles[room.inner] = tile_types.floor
        # tunnel to the previous room
        if len(rooms) > 0:
            for x, y in tunnel_between(rooms[-1].center, room.center):
                dungeon.tiles[x, y] = tile_types.floor
        rooms.append(room)
    return dungeon


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        # move horizontally and then vertically
        corner = x2, y1
    else:
        # move vertically and then horizontally
        corner = x1, y2
    for x, y in tcod.los.bresenham(start, corner).tolist():
        yield x, y
    for x, y in tcod.los.bresenham(corner, end).tolist():
        yield x, y

