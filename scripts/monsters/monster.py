import pyglet
from scripts import singletons, constants, projectile

class Monster(object):
    def __init__(self, x, y, room, sprite):
        self.hero = singletons.hero
        self.room = room
        self.x = x
        self.y = y

        self.sprite = pyglet.sprite.Sprite(sprite, x=self.x, y=self.y)

    def move(self):
        self.sprite.set_position(self.x, self.y)

    def attack(self):
        return
        print("waow")