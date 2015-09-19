
from hypothesis import strategies as st

from pg import gen
from pg import tiles

__all__ = (
    'create_test_tileset',
    'room',
    'small_size',
)

small_size = st.integers(min_value=1, max_value=16)


@st.composite
def room(draw):
    """A strategy that generates and returns rooms."""
    width = draw(small_size)
    height = draw(small_size)
    return gen.make_room(width, height, create_test_tileset())


def create_test_tileset():
    return tiles.TileSet(
        wall=tiles.Tile('wall'),
        floor=tiles.Tile('floor'),
    )
