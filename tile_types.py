from typing import Tuple

import numpy as np


# A NumPy struct compatible with Console.tiles_rgb
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # a Unicode codepoint
        ("fg", "3B"),  # 3 unsigned bytes representing an RGB foreground color
        ("bg", "3B"),  # 3 unsigned bytes representing an RGB background color
    ]
)
# Type alias for the Python type corresponding to the above NumPy type
Graphic = Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]

# A NumPy struct to hold statically-defined tile data
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # true if this tile can be traversed
        ("transparent", np.bool),  # false if this tile blocks FoV
        ("dark", graphic_dt),  # graphics for the tile when not in FoV
        ("light", graphic_dt),  # graphics for the tile when in FoV
    ]
)


def new_tile(
        *,
        walkable: bool,
        transparent: bool,
        dark: Graphic,
        light: Graphic,
) -> np.ndarray:
    """Constructor for `tile_dt` instances"""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# Fog graphic covers tiles that have not been explored and aren't in view.
FOG = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)
