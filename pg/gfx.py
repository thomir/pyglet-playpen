from pkg_resources import resource_stream
import pyglet


def run_tile_viewer(map):
    window = pyglet.window.Window()
    label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

    @window.event
    def on_draw():
        window.clear()
        draw_tile_map(map)

    @window.event
    def on_key_press(symbol, modifiers):
        print('A key was pressed')

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
