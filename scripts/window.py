import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from scripts import room, singletons, constants
from scripts.monsters import ghost, gargoyle, gremlin, lich, skeleton, shooting_monster
import random
import math

window = pyglet.window.Window(600,480,fullscreen = False)
window.set_mouse_visible(False)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

hero = singletons.hero
room1 = room.Room(1)
room2 = room.Room(2)
room2.left(room1)
room1.mons.append(lich.Lich(300,300, room1))
room1.mons.append(ghost.Ghost(200, 200, room1))
room1.mons.append(gargoyle.Gargoyle(400,200,room1,"right"))
room1.mons.append(gargoyle.Gargoyle(500,200,room1,"left"))
room1.mons.append(gargoyle.Gargoyle(500,150,room1,"up"))
room1.mons.append(gremlin.Gremlin(330,24,room1))
room1.mons.append(skeleton.Skeleton(80, 100, room1))

hero.setRoom(room1)
@window.event
def on_draw():
    if hero.transition != None:
        curRoom = hero.room
        if hero.transition == "Right" and hero.room.rightRoom != None:
            hero.x = 10
            hero.room = hero.room.rightRoom
            hero.transition = None
        if hero.transition == "Left" and hero.room.leftRoom != None:
            hero.x = constants.roomWidth - 10 - constants.playerWidth
            hero.room = hero.room.leftRoom
            hero.transition = None
        if hero.transition == "Up" and hero.room.upRoom != None:
            hero.y = 10
            hero.momy = 13
            hero.room = hero.room.upRoom
            hero.transition = None
        if hero.transition == "Down" and hero.room.downRoom != None:
            hero.y = constants.roomHeight - 10 - constants.playerHeight
            hero.momy = -4
            hero.room = hero.room.downRoom
            hero.transition = None
        if hero.transition == None:
            for mon in curRoom.mons:
                pyglet.clock.unschedule(mon.move)
                if issubclass(mon.__class__, shooting_monster.ShootingMonster):
                    for projectile in mon.projectiles:
                        pyglet.clock.unschedule(projectile.move)
                        projectile.alive = False
                        mon.projectiles.remove(projectile)
            for mon in hero.room.mons:
                pyglet.clock.schedule_interval(mon.move, 1/30)
        hero.transition = None
    
    window.clear()
    hero.room.batch.draw()
    if hero.invulnerabilityLeft % 2 == 0:
        hero.sprite.draw()
    hero.heart_batch.draw()
    hero.heartdraw()
    
    for mon in hero.room.mons:
        if mon.health < 1:
            pyglet.clock.unschedule(mon.move)
            hero.room.mons.remove(mon)
        else:
            if mon.invulnerability % 2 == 0:
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
    if button == key.SPACE:
        hero.attack()

@window.event
def on_key_release(button, modifiers):
    if button == key.LEFT:
        hero.direction["left"] = False
    if button == key.RIGHT:
        hero.direction["right"] = False

def run():
    for mon in hero.room.mons:
        pyglet.clock.schedule_interval(mon.move, 1/30)
    pyglet.clock.schedule_interval(hero.move, 1/30)
    
    pyglet.app.run()
