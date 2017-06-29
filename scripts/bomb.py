import pyglet
import math, random
from scripts import singletons, constants
from resources import resource_loader

class Bomb(object):

    def __init__(self, x = None, y = None, room = None, attack = None):
        
        self.x = x
        self.y = y
        self.room = room
        self.speedx = random.randint(-5,5)
        self.speedy = 10
        
        self.attack = attack
        self.alive = True
        self.exploding = False
        self.lifetime = 15

        
        self.graphic = pyglet.image.load(resource_loader.files["bomb.png"])
        self.boom = pyglet.image.load(resource_loader.files["boom.png"])
        self.sprite = pyglet.sprite.Sprite(self.graphic, x=self.x, y=self.y)
        
    def move(self, dt):
        if (self.alive):
            if self.exploding:
                self.lifetime -= 1
                if self.lifetime == 0:
                    self.alive = False
                return

            self.speedy -= 1
            self.x += self.speedx
            self.y += self.speedy

            if self.room.checkMove(self.y, self.x, constants.bombHeight, constants.bombWidth):
                self.exploding = True
                while self.room.checkMove(self.y, self.x, constants.bombHeight, constants.bombWidth):
                    if self.speedy < 0:
                        self.y += 1
                        self.x += self.speedx / self.speedy
                    else:
                        self.y -= 1
                        if self.speedy != 0:
                            self.x -= self.speedx / self.speedy
                        else:
                            self.x -= self.speedx
                            
                if self.room.checkPlayer(self.y - 5, self.x - 5, constants.bombHeight + 7, constants.bombWidth + 10, singletons.hero):
                    singletons.hero.hurt(self.attack)
                self.sprite.set_position(self.x - 3, self.y - 4)
                self.sprite.image = self.boom
            else:
                self.sprite.set_position(self.x, self.y)


