import pyglet
import math
import random
from scripts import singletons
from resources import resource_loader

class Ghost:
    
    def __init__(self, x, y):
        self.hero = singletons.Singleton.hero
        self.x = x
        self.y = y
        
        self.charge = 0
        self.charge_duration = 0
        self.charge_direction = (0,0)

        self.ghost_idle = pyglet.image.load(resource_loader.files["spoopy.png"])
        self.sprite = pyglet.sprite.Sprite(self.ghost_idle, x=self.x, y=self.y)
        
    def move(self, dt):
        
        if self.charge_duration > 0:
            self.charge_duration -= 1
            self.x += self.charge_direction[0] * 10
            self.y += self.charge_direction[1] * 10
            self.sprite.set_position(self.x, self.y)
            return
        
        if self.charge == 10:
            self.charge = 0
            self.charge_duration = 12
            self.charge_direction = (-((self.x - self.hero.x) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)), -((self.y - self.hero.y) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)))
            return
        
        if (self.x - self.hero.x)**2 + (self.y - self.hero.y)**2 > 10000:
            self.x -= ((self.x - self.hero.x) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 5
            self.y -= ((self.y - self.hero.y) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 5
            
        self.x += random.randint(0,6) - 3
        self.y += random.randint(0,6) - 3
        
        if (self.x - self.hero.x)**2 + (self.y - self.hero.y)**2 < 14400:
            self.charge += 1
        else:
            self.charge = 0
            
        self.sprite.set_position(self.x, self.y)