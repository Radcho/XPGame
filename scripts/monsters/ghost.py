import pyglet
import math
import random
from scripts import singletons, constants
from scripts.monsters import monster
from resources import resource_loader

class Ghost(monster.Monster):
    
    def __init__(self, x, y, room):
        self.ghost_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['ghost_left_' + str(i) + '.png']) for i in range(1, 6)], 1/16)
        self.ghost_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['ghost_right_' + str(i) + '.png']) for i in range(1, 6)], 1/16)
        self.ghost_charge_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['ghost_charge_left_' + str(i) + '.png']) for i in range(1, 6)], 1/16)
        self.ghost_charge_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['ghost_charge_right_' + str(i) + '.png']) for i in range(1, 6)], 1/16)

        super().__init__(x, y, room, self.ghost_right, constants.ghostWidth, constants.ghostHeight)
        self.attack = 1
        self.health = 2
        self.charge = 0
        self.charge_duration = 0
        self.charge_direction = (0,0)
        self.direction = "right"
        
    def move(self, dt):
        
        if self.charge_duration > 0:
            self.charge_duration -= 1
            self.x += self.charge_direction[0] * 5
            self.y += self.charge_direction[1] * 5
            
            if self.sprite.image != self.ghost_charge_left and self.direction == "left":
                self.sprite.image = self.ghost_charge_left
            elif self.sprite.image != self.ghost_charge_right and self.direction == "right":
                self.sprite.image = self.ghost_charge_right
            if self.room.checkPlayer(self.y, self.x, constants.ghostHeight, constants.ghostWidth, singletons.hero):
                singletons.hero.hurt(self.attack)
                
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

        if self.x > self.hero.x:
            self.direction = "left"
        else:
            self.direction = "right"

        if self.sprite.image != self.ghost_left and self.direction == "left":
            self.sprite.image = self.ghost_left
        elif self.sprite.image != self.ghost_right and self.direction == "right":
            self.sprite.image = self.ghost_right

        super().move()
