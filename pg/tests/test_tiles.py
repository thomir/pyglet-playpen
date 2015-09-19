from unittest import TestCase


from pg import tiles


class TileTests(TestCase):

    def test_equality(self):
        t1 = tiles.Tile("one")
        t1_ = tiles.Tile("one")
        t2 = tiles.Tile("two")

        self.assertNotEqual(t1, t2)
        self.assertEqual(t1, t1_)
