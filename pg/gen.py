"""First attempt at generation.

This is the simplest algorithm that might possibly work.
"""

from collections import (
    defaultdict,
    namedtuple,
)

from pg.tiles import (
    Tile,
    TileSet,
)


class Bounds:
    def __init__(self):
        self.min = None
        self.max = None

    def difference(self):
        if self.min is None or self.max is None:
            return 0
        else:
            return (self.max - self.min) + 1

    def update(self, num: int):
        if self.min is None or self.max is None:
            self.min = self.max = num
        else:
            self.min = min(self.min, num)
            self.max = max(self.max, num)


class Map:
    """A map that stores tile arrangements with an arbitrary dimension.

    Tiles are stored with dimensions that can be any value at all, and tile
    dimensions are normalised to start at 0,0 and all be positive on output.

    """

    def __init__(self):
        self._data = defaultdict(lambda: dict())
        self._x_bounds = Bounds()
        self._y_bounds = Bounds()

    def set_tile(self, x: int, y: int, tile):
        """Set a tile at a given position."""
        self._x_bounds.update(x)
        self._y_bounds.update(y)
        self._data[x][y] = tile

    def get_tile(self, x: int, y: int):
        """Get a tile at a given position, or None if no tile set."""
        # We shouldn't use:
        # self._data[x][y]
        # ...here, since it will create a new dict object if the tile does not
        # exist. So instead, do some checking first:
        if x not in self._data or y not in self._data[x]:
            return None
        return self._data[x][y]

    def get_width(self):
        return self._x_bounds.difference()

    def get_height(self):
        return self._y_bounds.difference()

    def is_normalised(self):
        return self._x_bounds.min in (0, None) \
            and self._y_bounds.min in (0, None)

    def get_normalised_map(self):
        """Get a copy of this map with the map bounds starting at (0,0)."""
        if self.is_normalised():
            return self
        normalised_map = Map()
        x_offset = 0 - self._x_bounds.min
        y_offset = 0 - self._y_bounds.min
        for x in self._data:
            for y in self._data[x]:
                normalised_map.set_tile(
                    x + x_offset,
                    y + y_offset,
                    self._data[x][y]
                )
        return normalised_map

    def get_tiles(self):
        """A generator that returns (x, y, tile) tuples."""
        for x in self._data:
            for y in self._data[x]:
                yield (x, y, self._data[x][y])

    def compose_map(self, map, x, y, safe=True):
        """Copy the contents of 'map' into this map, starting at (x, y).

        If 'safe' is True (the default), ValueError will be raised if this
        operation would overwrite tiles in the map.

        If 'safe' is False, the tiles in 'map' will overwrite any tiles in
        this map.

        Note that if 'map' is not normalised, the empty space in 'map' will be
        copied to this map as well.
        """
        if safe:
            for tile_x, tile_y, tile in map.get_tiles():
                dx = x + tile_x
                dy = y + tile_y
                if self.get_tile(dx, dy) is not None:
                    raise ValueError(
                        "This operation would overwrite a tile at (%d, %d) "
                        "in the destination map." % (dx, dy)
                    )

        for tile_x, tile_y, tile in map.get_tiles():
            self.set_tile(x + tile_x, y + tile_y, map.get_tile(x, y))


def make_room(width: int, height: int, tileset: TileSet) -> Map:
    if width <= 0 or height <= 0:
        raise ValueError("Width and Height parameters must both be > 0")
    room = Map()
    for x in range(width):
        for y in range(height):
            if x == 0 or y == 0 or x == width-1 or y == height-1:
                tile = tileset['wall']
            else:
                tile = tileset['floor']
            room.set_tile(x, y, tile)
    return room
