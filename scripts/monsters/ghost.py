import pyglet
import math
import random
from scripts import singletons
from scripts.monsters import monster
from resources import resource_loader

class Ghost(monster.Monster):
    
    def __init__(self, x, y, room):
        self.ghost_idle = pyglet.image.load(resource_loader.files["spoopy.png"])

        super().__init__(x, y, room, self.ghost_idle)

        self.charge = 0
        self.charge_duration = 0
        self.charge_direction = (0,0)
        
    def move(self, dt):
        
        if self.charge_duration > 0:
            self.charge_duration -= 1
            self.x += self.charge_direction[0] * 5
            self.y += self.charge_direction[1] * 5
            super().move()
            return
        
        if self.charge == 20:
            self.charge = 0
            self.charge_duration = 24
            self.charge_direction = (-((self.x - self.hero.x) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)), -((self.y - self.hero.y) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)))
            return
        
        if (self.x - self.hero.x)**2 + (self.y - self.hero.y)**2 > 10000:
            self.x -= ((self.x - self.hero.x) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 3
            self.y -= ((self.y - self.hero.y) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 3
            
        self.x += random.randint(0,4) - 2
        self.y += random.randint(0,4) - 2
        
        if (self.x - self.hero.x)**2 + (self.y - self.hero.y)**2 < 14400:
            self.charge += 1
        else:
            self.charge = 0
            
        super().move()