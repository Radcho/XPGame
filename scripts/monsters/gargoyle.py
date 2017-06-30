import pyglet
import math
from scripts import singletons, constants, projectile
from scripts.monsters import shooting_monster
from resources import resource_loader

class Gargoyle(shooting_monster.ShootingMonster):
    
    def __init__(self, x, y, room, direction):
        fireball_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['fireball_' + str(i) + '.png']) for i in range(1, 7)], 1/8)
        self.gargoyle_1_sprite = pyglet.image.load(resource_loader.files['gargoyle_' + direction + '_1.png'])
        self.gargoyle_2_sprite = pyglet.image.load(resource_loader.files['gargoyle_' + direction + '_2.png'])
        self.gargoyle_3_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['gargoyle_' + direction + '_3_' + str(i) + '.png']) for i in range(1, 3)], 1/8)
        self.gargoyle_4_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['gargoyle_' + direction + '_4_' + str(i) + '.png']) for i in range(1, 3)], 1/8)

        super().__init__(x, y, room, self.gargoyle_1_sprite, constants.gargWidth, constants.gargHeight, fireball_anim, 80)

        self.health = 2
        self.attack = 2

        directionDictionary = {"left":(1,0) , "right":(-1,0) , "up":(0,1) , "down":(0,-1)}
        self.direction = directionDictionary[direction]

    def move(self, dt):
        if (self.x*self.direction[0] >= self.hero.x*self.direction[0] and self.y*self.direction[1] <= self.hero.y*self.direction[1]):
            asleep = False
            if self.delay == 0:
                self.delay = 80
                self.addProjectile(self.x + (constants.gargWidth - constants.projWidth) // 2, self.y + (constants.gargHeight - constants.projWidth) // 2, self.hero.x, self.hero.y, self.attack)
        else:
            asleep = True
            self.delay = 80

        if asleep:
                self.sprite.image = self.gargoyle_1_sprite
        elif self.delay >= 50:
                self.sprite.image = self.gargoyle_2_sprite
        elif self.delay >= 20 and self.sprite.image != self.gargoyle_3_anim:
                self.sprite.image = self.gargoyle_3_anim
        elif self.delay <= 19 and self.sprite.image != self.gargoyle_4_anim:
                self.sprite.image = self.gargoyle_4_anim
        
        super().move()
