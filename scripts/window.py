import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from scripts import ghost, room, singletons, lich
import random
import math

window = pyglet.window.Window(600,480,fullscreen = False)
window.set_mouse_visible(False)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

hero = singletons.Singleton.hero
ghost = ghost.Ghost(200, 200)
room = room.Room()
lich = lich.Lich(300,300, room)
hero.setRoom(room)

@window.event
def on_draw():
    window.clear()
    room.batch.draw()
    hero.sprite.draw()
    ghost.sprite.draw()
    lich.sprite.draw()
    if lich.ice1.x != None:
        lich.ice1.sprite.draw()
    if lich.ice2.x != None:
        lich.ice2.sprite.draw()    

@window.event
def on_key_press(button, modifiers):
    if button == key.LEFT:
        hero.direction["left"] = True
    if button == key.RIGHT:
        hero.direction["right"] = True
    if button == key.UP:
        hero.jump()

@window.event
def on_key_release(button, modifiers):
    if button == key.LEFT:
        hero.direction["left"] = False
    if button == key.RIGHT:
        hero.direction["right"] = False

def run():
    pyglet.clock.schedule_interval(ghost.move, 1/15)
    pyglet.clock.schedule_interval(lich.move, 1/15)
    pyglet.clock.schedule_interval(hero.move, 1/30)
    pyglet.app.run()
