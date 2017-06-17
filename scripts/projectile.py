import pyglet
import math
from scripts import singletons, constants
from resources import resource_loader

class Projectile(object):

    def __init__(self, x = None, y = None, destx = None, desty = None, room = None, graphic = None):
        
        self.x = x
        self.y = y
        self.room = room
        self.direction = (-((self.x - destx) / math.sqrt((self.x - destx)**2 + (self.y - desty)**2)), -((self.y - desty) / math.sqrt((self.x - destx)**2 + (self.y - desty)**2)))

        self.alive = True

        self.sprite = pyglet.sprite.Sprite(graphic, x=self.x, y=self.y)
        
    def move(self, dt):
        if (self.alive):
            self.x += self.direction[0]*3
            self.y += self.direction[1]*3
            
            if self.room.checkMove(self.y, self.x, constants.projHeight, constants.projWidth):
                self.alive = False
            else:
                self.sprite.set_position(self.x, self.y)