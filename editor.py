import pyglet
from pyglet.window import mouse
from pyglet.gl import *
from resources import resource_loader

window = pyglet.window.Window(600,480,fullscreen = False)
window.set_mouse_visible(True)
mapa = []
for i in range(20):
    mapa.append([])
    for j in range(20):
        mapa[i].append(0)

b = pyglet.image.TileableTexture.create_for_image(pyglet.image.load(resource_loader.files['Background.png']))
w = pyglet.image.load(resource_loader.files['Wall.png'])
s = []
@window.event
def on_draw():
    window.clear()
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 1:
                w.blit(j * 30, i * 24)
            else:
                b.blit(j * 30, i * 24)

@window.event
def on_key_press(button, modifiers):
    if button == pyglet.window.key.SPACE:
        print(mapa)

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if modifiers & pyglet.window.key.MOD_SHIFT:
            for i in range(20):
                mapa[y//24][i] = 1 - mapa[y//24][i]
        elif modifiers & pyglet.window.key.MOD_CTRL:
            for i in range(20):
                mapa[i][x//30] = 1 - mapa[i][x//30]
        else:
            mapa[y//24][x//30] = 1 - mapa[y//24][x//30]
    else:
        print(x,y)
            



pyglet.app.run()
