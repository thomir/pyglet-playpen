
from pg import gen
from pg.gfx import run_tile_viewer
from pg import tiles

import random


def main():
    tileset = tiles.TileSet(
        wall=tiles.Tile((5, 0)),
        floor=tiles.Tile((1, 0)),
    )
    map = gen.make_room(10, 10)
    for i in range(10):
        try:
            map.compose_map(
                gen.make_room(
                    random.randint(5, 15),
                    random.randint(5, 15),
                ),
                random.randint(0, 50),
                random.randint(0, 50),
                safe=False,
            )
        except ValueError:
            pass

    map = map.get_normalised_map()
    run_tile_viewer(map, tileset)
