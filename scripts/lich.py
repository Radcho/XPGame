import pyglet
import math
from scripts import singletons, constants, projectile, functions
from resources import resource_loader

class Lich:
    
    def __init__(self, x, y, room):
        self.hero = singletons.Singleton.hero
        self.x = x
        self.y = y

        self.delay = 60
        self.casting = 0
        self.currentRoom = room


        self.ice1 = projectile.Projectile()
        self.ice2 = projectile.Projectile()

        self.lich_idle = pyglet.image.load(resource_loader.files["spoopy.png"])
        self.sprite = pyglet.sprite.Sprite(self.lich_idle, x=self.x, y=self.y)
        
    def move(self, dt):
        self.delay -= 1
        
        if self.delay == 0:
            self.delay = 75
            self.casting = 15

        elif self.casting != 0:
            self.casting -= 1
            if self.casting == 0:
                if self.ice1.x == None:
                    self.ice1 = projectile.Projectile(self.x, self.y, self.hero.x, self.hero.y, self.currentRoom, "ice")
                    pyglet.clock.schedule_interval(self.ice1.move, 1/15)
                elif self.ice2.x == None:
                    self.ice2 = projectile.Projectile(self.x, self.y, self.hero.x, self.hero.y, self.currentRoom, "ice")
                    pyglet.clock.schedule_interval(self.ice2.move, 1/15)

        else:
            movex = 0
            movey = 0
            if (self.x - self.hero.x)**2 + (self.y - self.hero.y)**2 > 150**2:
                movex = -((self.x - self.hero.x) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 4
                movey = -((self.y - self.hero.y) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 4

            elif (self.x - self.hero.x)**2 + (self.y - self.hero.y)**2 < 110**2:
                movex = ((self.x - self.hero.x) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 2
                movey = ((self.y - self.hero.y) / math.sqrt((self.x - self.hero.x)**2 + (self.y - self.hero.y)**2)) * 2
            
            if functions.checkMove(self.y + movey, self.x, constants.lichHeight, constants.lichWidth, self.currentRoom):
                movey = 0
            if functions.checkMove(self.y, self.x + movex, constants.lichHeight, constants.lichWidth, self.currentRoom) or functions.checkMove(self.y + movey, self.x + movex, constants.lichHeight, constants.lichWidth, self.currentRoom):
                movex = 0
                
            self.x += movex
            self.y += movey

        self.sprite.set_position(self.x, self.y)





        
