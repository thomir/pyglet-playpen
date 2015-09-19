from pkg_resources import resource_stream
import pyglet


def run_tile_viewer(map):
    window = pyglet.window.Window(
        fullscreen=True
    )

    @window.event
    def on_draw():
        window.clear()
        draw_tile_map(map)

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            window.close()

    pyglet.app.run()


def get_tile_image(tile_name):
    tile_filename = tile_name + '.png'
    tile_stream = resource_stream('pg.tiles', tile_filename)
    return pyglet.image.load(tile_filename, file=tile_stream)


def get_tile_size():
    return 16


def draw_tile_map(map):
    tilesize = get_tile_size()
    for tx, ty, tile in map.get_tiles():
        x = tx * tilesize
        y = ty * tilesize
        image = get_tile_image(tile.name)
        image.blit(x, y)
