import pyglet
import math
from scripts import singletons, constants, projectile
from scripts.monsters import shooting_monster
from resources import resource_loader

class Gargoyle(shooting_monster.ShootingMonster):
    
    def __init__(self, x, y, room, direction):
        fireball_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['fireball_' + str(i) + '.png']) for i in range(1, 7)], 1/8)
        self.gargoyle_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['gargoyle_' + direction + '_' + str(i) + '.png']) for i in range(1, 2)], 1/16)

        super().__init__(x, y, room, self.gargoyle_anim, fireball_anim, 120)

        directionDictionary = {"left":(1,0) , "right":(-1,0) , "up":(0,1) , "down":(0,-1)}
        self.direction = directionDictionary[direction]

    def move(self, dt):
        if (self.x*self.direction[0] >= self.hero.x*self.direction[0] and self.y*self.direction[1] <= self.hero.y*self.direction[1]):
            if self.delay == 0:
                self.delay = 120
                self.addProjectile(self.x, self.y, self.hero.x, self.hero.y)
        else:
            self.delay = 120
            
        super().move()