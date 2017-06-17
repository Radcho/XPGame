import pyglet
import math
from scripts import singletons, constants, projectile
from scripts.monsters import shooting_monster
from resources import resource_loader

class Lich(shooting_monster.ShootingMonster):
    
    def __init__(self, x, y, room):
        self.lich_walking_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['lich_right_' + str(i) + '.png']) for i in range(1, 2)], 1/16)
        self.lich_walking_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['lich_left_' + str(i) + '.png']) for i in range(1, 2)], 1/16)
        
        iceball_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['iceball_' + str(i) + '.png']) for i in range(1, 7)], 1/8)

        super().__init__(x, y, room, self.lich_walking_right, iceball_anim, 60)
        
    def move(self, dt):        
        if self.delay < 16:
            if self.delay == 0:
                self.delay = 90
                self.addProjectile(self.x, self.y, self.hero.x, self.hero.y)
        else:
            movex = 0
            movey = 0
            if (self.x - self.hero.x)**2 + (self.y - self.hero.y)**2 > 150**2:
                movex = -((self.x - self.hero.x) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 4
                movey = -((self.y - self.hero.y) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 4

            elif (self.x - self.hero.x)**2 + (self.y - self.hero.y)**2 < 110**2:
                movex = ((self.x - self.hero.x) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 2
                movey = ((self.y - self.hero.y) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 2
            
            if self.room.checkMove(self.y + movey, self.x, constants.lichHeight, constants.lichWidth):
                movey = 0
            if self.room.checkMove(self.y, self.x + movex, constants.lichHeight, constants.lichWidth) or self.room.checkMove(self.y + movey, self.x + movex, constants.lichHeight, constants.lichWidth):
                movex = 0                

            self.x += movex
            self.y += movey

        self.sprite.image = self.lich_walking_left if self.x > self.hero.x else self.lich_walking_right
        super().move()