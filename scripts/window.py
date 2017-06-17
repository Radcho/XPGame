import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from scripts import room, singletons
from scripts.monsters import ghost, gargoyle, gremlin, lich, skeleton, shooting_monster
import random
import math

window = pyglet.window.Window(600,480,fullscreen = False)
window.set_mouse_visible(False)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

hero = singletons.hero
mons = []
mons.append(ghost.Ghost(200, 200, room))
room = room.Room()
mons.append(lich.Lich(300,300, room))
mons.append(gargoyle.Gargoyle(400,200,room,"right"))
mons.append(gargoyle.Gargoyle(500,200,room,"left"))
mons.append(gargoyle.Gargoyle(500,150,room,"up"))
mons.append(gremlin.Gremlin(330,24,room))
mons.append(skeleton.Skeleton(80, 100, room))

hero.setRoom(room)

@window.event
def on_draw():
    window.clear()
    room.batch.draw()
    hero.sprite.draw()
    hero.heart_batch.draw()
    hero.heartdraw()

    for mon in mons:
        mon.sprite.draw()
        if issubclass(mon.__class__, shooting_monster.ShootingMonster):
            for projectile in mon.projectiles:
                projectile.sprite.draw()

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
    for mon in mons:
        pyglet.clock.schedule_interval(mon.move, 1/30)
    pyglet.clock.schedule_interval(hero.move, 1/30)
    
    pyglet.app.run()
