import pyglet
import math
from scripts import singletons, constants, projectile
from scripts.monsters import shooting_monster
from resources import resource_loader

class Lich(shooting_monster.ShootingMonster):
    
    def __init__(self, x, y, room):
        self.lich_moving = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['lich_' + str(i) + '.png']) for i in range(1, 5)], 1/16)
        self.lich_casting = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['lich_cast_' + str(i) + '.png']) for i in range(1, 3)], 1/16)
        iceball_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['iceball_' + str(i) + '.png']) for i in range(1, 7)], 1/8)
        self.health = 2
        self.attack = 1
        super().__init__(x, y, room, self.lich_moving, constants.lichWidth, constants.lichHeight, iceball_anim, 60)
        
    def move(self, dt):        
        if self.delay < 16:
            if self.delay == 0:
                self.delay = 90
                self.addProjectile(self.x + constants.lichWidth // 2, self.y + constants.lichHeight // 2, self.hero.x, self.hero.y, self.attack)
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

        if (self.delay < 16 and self.sprite.image != self.lich_casting):
            self.sprite.image = self.lich_casting
        elif (self.sprite.image != self.lich_moving):
            self.sprite.image = self.lich_moving
        super().move()
