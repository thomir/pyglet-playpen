
from pg import gen
from pg.gfx import run_tile_viewer
from pg import tiles


def main():
    tileset = tiles.TileSet(
        wall=tiles.Tile('wall'),
        floor=tiles.Tile('floor'),
    )
    map = gen.make_room(10, 10, tileset)
    run_tile_viewer(map)
