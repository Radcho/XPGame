import pyglet
import math
from scripts import singletons, constants, functions
from resources import resource_loader

class Projectile:

    def __init__(self, x = None, y = None, destx = None, desty = None, room = None, graphic = None):
        
        self.x = x
        if self.x == None:
            return
        self.y = y
        self.currentRoom = room
        self.direction = (-((self.x - destx) / math.sqrt((self.x - destx)**2 + (self.y - desty)**2)), -((self.y - desty) / math.sqrt((self.x - destx)**2 + (self.y - desty)**2)))
        graphic_list = {"ice":"spoopy.png", "fire":"spoopy.png", "arrow":"spoopy.png"}
        self.iceball = pyglet.image.load(resource_loader.files[graphic_list[graphic]])
        self.sprite = pyglet.sprite.Sprite(self.iceball, x=self.x, y=self.y)
        
    def move(self, dt):
        if self.x == None:
            return
        self.x += self.direction[0]*5
        self.y += self.direction[1]*5
        
        
        if functions.checkMove(self.y, self.x, constants.iceHeight, constants.iceWidth, self.currentRoom):
            self.x = None
        else:
            self.sprite.set_position(self.x, self.y)
