from functools import partial, lru_cache

from pkg_resources import resource_stream

import math

import pyglet
from pyglet import gl


def run_tile_viewer(map):
    app = TileViewerApp(map)
    pyglet.app.run()


class TileViewerApp:

    def __init__(self, map):
        config = gl.Config()
        config.double_buffer = True
        self.window = pyglet.window.Window(
            fullscreen=True,
            config=config,
        )

        self.window.on_draw = self.on_draw

        # pyglet.clock.set_fps_limit(60)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.update, 1.0 / 60.0)
        self.fps_display = pyglet.clock.ClockDisplay()

        self.tile_renderer = TileMapRenderer(map)
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


def get_tile_size():
    return 16


class TileMapRenderer:

    """Loads resources for, and renders a tile map."""

    def __init__(self, tilemap):
        self._map = tilemap
        self._tiles = []
        tilesize = get_tile_size()
        for tx, ty, tile in self._map.get_tiles():
            x = tx * tilesize
            y = ty * tilesize
            self._tiles.append(DrawnTile(x, y, tile.name, tilesize))

    def draw_tile_map(self):
        for t in self._tiles:
            t.draw()


class DrawnTile:

    def __init__(self, x, y, name, tilesize):
        self.verts = pyglet.graphics.vertex_list(
            6,
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
                't2f',
                (
                    0.0, 0.0,
                    1.0, 0.0,
                    1.0, 1.0,
                    1.0, 1.0,
                    0.0, 1.0,
                    0.0, 0.0,
                )
            )
        )
        self.tile_name = name
        self.image = get_tile_image(name)
        self.texture = self.image.get_texture()

    def draw(self):
        gl.glEnable(self.texture.target)        # typically target is GL_TEXTURE_2D
        gl.glBindTexture(self.texture.target, self.texture.id)
        self.verts.draw(gl.GL_TRIANGLES)


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
