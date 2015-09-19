from unittest import TestCase

from hypothesis import assume, given
from hypothesis import strategies as st

from pg import gen
from pg import tiles
from pg.tests import strategies as pgst


class TestMap(TestCase):

    def test_get_width_on_empty_map(self):
        m = gen.Map()
        self.assertEqual(0, m.get_width())

    def test_get_height_on_empty_map(self):
        m = gen.Map()
        self.assertEqual(0, m.get_height())

    def test_get_tile_returns_none_for_unset_tile(self):
        m = gen.Map()
        self.assertIsNone(m.get_tile(0, 0))

    @given(st.integers(), st.integers())
    def test_get_returns_a_tile_we_set(self, x, y):
        m = gen.Map()
        tile = tiles.Tile("test_tile")
        m.set_tile(x, y, tile)
        self.assertEqual(tile, m.get_tile(x, y))

    def test_normalising_empty_map(self):
        m = gen.Map()
        self.assertTrue(m.is_normalised())
        m2 = m.get_normalised_map()
        self.assertEqual(m, m2)

    def test_single_tile_map_is_normalised(self):
        m = gen.Map()
        m.set_tile(0, 0, tiles.Tile("test_tile"))
        self.assertTrue(m.is_normalised())
        m2 = m.get_normalised_map()
        self.assertEqual(m, m2)

    def test_get_tiles_on_empty_map(self):
        m = gen.Map()
        self.assertEqual([], list(m.get_tiles()))

    @given(st.integers(), st.integers())
    def test_get_tiles_on_single_tile_map(self, x, y):
        m = gen.Map()
        tile = tiles.Tile("test")
        m.set_tile(x, y, tile)
        self.assertEqual([(x, y, tile)], list(m.get_tiles()))

    @given(st.integers(), st.integers())
    def test_normalising_single_tile_map(self, x, y):
        assume(x != 0 and y != 0)
        m = gen.Map()
        tile = tiles.Tile("test_tile")
        m.set_tile(x, y, tile)

        self.assertFalse(m.is_normalised())
        m2 = m.get_normalised_map()
        self.assertNotEqual(m, m2)
        self.assertEqual(1, m2.get_height())
        self.assertEqual(1, m2.get_width())
        self.assertEqual(tile, m2.get_tile(0, 0))

    @given(pgst.small_size, pgst.small_size)
    def test_compose_single_normalised_map(self, width, height):
        m1 = gen.Map()
        m2 = gen.Map()
        m2.set_tile(0, 0, tiles.Tile("test"))
        m2.set_tile(width - 1, height - 1, tiles.Tile("test"))
        m1.compose_map(m2, 0, 0)

        self.assertEqual(width, m1.get_width())
        self.assertEqual(height, m1.get_height())

    @given(st.integers(), st.integers())
    def test_compose_raises_ValueError_on_overwrite_to_self(self, x, y):
        m = gen.Map()
        m.set_tile(x, y, tiles.Tile("test"))
        with self.assertRaises(ValueError):
            m.compose_map(m, 0, 0)

    @given(pgst.room(), pgst.room())
    def test_compose_raises_ValueError_on_overwrite(self, room1, room2):
        m = gen.Map()
        m.compose_map(room1, 0, 0)
        with self.assertRaises(ValueError):
            m.compose_map(room2, 0, 0)

    @given(pgst.room(), pgst.room())
    def test_compose_multiple_rooms(self, room1, room2):
        m = gen.Map()
        m.compose_map(room1, 0, 0)
        m.compose_map(room2, room1.get_width(), room1.get_height())
        self.assertEqual(
            room1.get_width() + room2.get_width(),
            m.get_width()
        )
        self.assertEqual(
            room1.get_height() + room2.get_height(),
            m.get_height()
        )


class TestBounds(TestCase):

    def test_empty_bounds(self):
        bounds = gen.Bounds()
        self.assertEqual(0, bounds.difference())

    @given(st.integers())
    def test_single_unit_bounds(self, num):
        bounds = gen.Bounds()
        bounds.update(num)
        self.assertEqual(1, bounds.difference())

    @given(st.integers(), st.integers())
    def test_multiple_unit_bounds(self, left, right):
        bounds = gen.Bounds()
        bounds.update(left)
        bounds.update(right)
        expected = (max(left, right) - min(left, right)) + 1
        self.assertEqual(expected, bounds.difference())


class TestRoomGeneration(TestCase):

    def setUp(self):
        super().setUp()
        self.tileset = pgst.create_test_tileset()

    def test_creates_map(self):
        room = gen.make_room(10, 10, self.tileset)
        self.assertIsInstance(room, gen.Map)

    @given(pgst.small_size, pgst.small_size)
    def test_map_is_the_correct_size(self, width, height):
        room = gen.make_room(width, height, self.tileset)
        self.assertEqual(width, room.get_width())
        self.assertEqual(height, room.get_height())

    @given(st.integers(max_value=0), st.integers(max_value=0))
    def test_invalid_sizes(self, width, height):
        with self.assertRaises(ValueError):
            gen.make_room(width, height, self.tileset)

    @given(pgst.small_size, pgst.small_size)
    def test_rooms_are_normalised(self, width, height):
        room = gen.make_room(width, height, self.tileset)
        self.assertTrue(room.is_normalised())
