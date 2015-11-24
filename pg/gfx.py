from collections import defaultdict
from functools import lru_cache
import itertools

from pkg_resources import resource_stream

import math

import pyglet
from pyglet import gl


def run_tile_viewer(map, tileset):
    # pyglet.options['debug_graphics_batch'] = True
    app = TileViewerApp(map, tileset)
    gl.glEnable(gl.GL_TEXTURE_2D)

    pyglet.app.run()


class TileViewerApp:

    def __init__(self, map, tileset):
        config = gl.Config()
        config.double_buffer = True
        self.window = pyglet.window.Window(
            fullscreen=True,
            config=config,
            vsync=False,
        )

        self.window.on_draw = self.on_draw

        # pyglet.clock.set_fps_limit(60)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        pyglet.clock.schedule_interval(self.update, 1.0 / 60.0)
        self.fps_display = pyglet.clock.ClockDisplay()

        self.tile_renderer = TileMapRenderer(map, tileset)
        self.camera = Camera()

    def on_draw(self):
        self.camera.focus(self.window.width, self.window.height)
        self.window.clear()
        self.tile_renderer.draw_tile_map()
        self.fps_display.draw()

    def update(self, dt):
        if self.keys[pyglet.window.key.ESCAPE]:
            self.window.close()
        if self.keys[pyglet.window.key.LEFT]:
            self.camera.x -= 100 * dt
        if self.keys[pyglet.window.key.RIGHT]:
            self.camera.x += 100 * dt
        if self.keys[pyglet.window.key.UP]:
            self.camera.y += 100 * dt
        if self.keys[pyglet.window.key.DOWN]:
            self.camera.y -= 100 * dt
        if self.keys[pyglet.window.key.PAGEUP]:
            self.camera.scale = max(1, self.camera.scale - 10)
        if self.keys[pyglet.window.key.PAGEDOWN]:
            self.camera.scale = min(1000, self.camera.scale + 10)


@lru_cache(maxsize=None)
def get_tile_image(tile_name):
    tile_filename = tile_name + '.png'
    tile_stream = resource_stream('pg.tiles', tile_filename)
    return pyglet.image.load(tile_filename, file=tile_stream)


class TileLibrary:

    def __init__(self, filename, rows, columns):
        self.image = get_tile_image(filename)
        self.image_grid = pyglet.image.ImageGrid(self.image, rows, columns)
        self.texture_grid = pyglet.image.TextureGrid(self.image_grid)

    def get_texture_coords_for_tile(self, row, column):
        # The texture coords need some processing. We get 3D coords for a
        # quad, but we need 2D coords for two triangles.
        coords = self.texture_grid[(row, column)].tex_coords
        # First, filter out every third element, converting X,Y,Z triplets
        # into (X,Y) pairs:
        coords_2d = tuple(zip(coords[0::3], coords[1::3]))
        # Now turn the quad into two triples:
        return tuple(itertools.chain(
            coords_2d[0],
            coords_2d[1],
            coords_2d[2],
            coords_2d[2],
            coords_2d[3],
            coords_2d[0],
        ))

    def get_id(self):
        return self.texture_grid.id


def get_tile_size():
    return 16


class TileMapRenderer:

    """Loads resources for, and renders a tile map."""

    def __init__(self, tilemap, tileset):
        self._tile_set = tileset
        self._tile_library = TileLibrary('set_0', 6, 7)
        self._map = tilemap
        # self._tiles = []
        tilesize = get_tile_size()
        self.tile_batch = pyglet.graphics.Batch()

        for tx, ty, tile_name in self._map.get_tiles():
            x = tx * tilesize
            y = ty * tilesize
            self.tile_batch.add(
                6,
                gl.GL_TRIANGLES,
                None,  # no group.
                (
                    'v2i\static',
                    (
                        x, y,
                        x + tilesize, y,
                        x + tilesize, y + tilesize,
                        x + tilesize, y + tilesize,
                        x, y + tilesize,
                        x, y,
                    )
                ),
                (
                    't2f\static', self._tile_library.get_texture_coords_for_tile(
                        *self._tile_set[tile_name].name
                    )
                )
            )

    def draw_tile_map(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tile_library.get_id())
        self.tile_batch.draw()


class Camera:

    def __init__(self):
        self.x = self.y = 0
        self.angle = 0
        self.scale = 300

    def focus(self, window_width, window_height):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = window_width / window_height
        gl.gluOrtho2D(
            -self.scale * aspect,
            +self.scale * aspect,
            -self.scale,
            +self.scale,
        )
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.gluLookAt(
            self.x, self.y, 1.0,   # camera position
            self.x, self.y, -1.0,  # thing we're looking at
            math.sin(self.angle), math.cos(self.angle), 0.0
        )
