

class Tile:

    """The Tile class represents a single tile type."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tile: %r>" % self.name

    def __eq__(self, other):
        return other.name == self.name


class TileSet(dict):

    """Store a series of specific tiles for a particular theme."""
