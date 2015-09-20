
from pg import gen
from pg.gfx import run_tile_viewer
from pg import tiles

import random


def main():
    tileset = tiles.TileSet(
        wall=tiles.Tile('wall'),
        floor=tiles.Tile('floor'),
    )
    map = gen.make_room(10, 10, tileset)
    for i in range(10):
        try:
            map.compose_map(
                gen.make_room(
                    random.randint(5, 15),
                    random.randint(5, 15),
                    tileset,
                ),
                random.randint(0, 50),
                random.randint(0, 50),
            )
        except ValueError:
            pass

    map = map.get_normalised_map()
    run_tile_viewer(map)
