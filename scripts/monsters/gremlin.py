import pyglet
import math
from scripts import singletons, constants
from scripts.monsters import monster
from resources import resource_loader

class Gremlin(monster.Monster):
    
    def __init__(self, x, y, room):
        self.gremlin_walking_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['gremlin_right_' + str(i) + '.png']) for i in range(1, 5)], 1/16)
        self.gremlin_walking_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['gremlin_left_' + str(i) + '.png']) for i in range(1, 5)], 1/16)
        self.gremlin_attacking_right = pyglet.image.load(resource_loader.files['gremlin_right_attack.png'])
        self.gremlin_attacking_left = pyglet.image.load(resource_loader.files['gremlin_left_attack.png'])
        super().__init__(x, y, room, self.gremlin_walking_right, constants.gremlinWidth, constants.gremlinHeight)

        self.fallSpeed = 0
        self.jumping = False

        self.health = 3
        self.att = 2

        self.direction = "left"
        self.attackDelay = -1
        self.attacking = False
        self.range = 10
        
    def move(self, dt):
        self.fallSpeed -= 1
        endAttack = False
        if not self.attacking and not ((self.x <= self.hero.x + constants.playerWidth + self.range and self.hero.x <= self.x + constants.gremlinWidth + self.range) and abs(self.y - self.hero.y) < constants.tileHeight*3):
        
            self.direction = "right"
            move = 2
            if self.x >= self.hero.x:
                move = -2
                self.direction = "left"

            if self.room.checkMove(self.y, self.x + move, constants.gremlinHeight, constants.gremlinWidth):
                move = 0

        else:
            move = 0
            if self.attackDelay == -1:
                self.attacking = True
                self.attackDelay = 20
                if self.x >= self.hero.x:
                    self.direction = "left"
                else:
                    self.direction = "right"
            else:
                self.attackDelay -= 1
            if self.attackDelay == 0:
                self.attacking = False
                self.attackDelay = -1
                self.attack()
                endAttack = True
                
        if self.room.checkMove(self.y + self.fallSpeed, self.x, constants.gremlinHeight, constants.gremlinWidth):
            if self.fallSpeed < 0:
                self.jumping = False
            self.fallSpeed = 0

        if self.room.checkMove(self.y + self.fallSpeed, self.x + move, constants.gremlinHeight, constants.gremlinWidth):
            move = 0
        
        self.x += move
        self.y += self.fallSpeed
        
        if self.fallSpeed == 0 and move == 0 and not self.jumping and not self.attacking and not endAttack:
            self.jumping = True
            self.fallSpeed = 11

        if not self.attacking:
            if self.sprite.image != self.gremlin_walking_left and self.direction == "left":
                self.sprite.image = self.gremlin_walking_left
            elif self.sprite.image != self.gremlin_walking_right and self.direction == "right":
                self.sprite.image = self.gremlin_walking_right
        else:
            if self.sprite.image != self.gremlin_attacking_left and self.direction == "left":
                self.sprite.image = self.gremlin_attacking_left
            elif self.sprite.image != self.gremlin_attacking_right and self.direction == "right":
                self.sprite.image = self.gremlin_attacking_right

        super().move()

    def attack(self):
        if self.direction == "left":
            if self.room.checkPlayer(self.y, self.x - 2*self.range, constants.gremlinHeight, 2*self.range, singletons.hero):
                singletons.hero.hurt(self.att)
        else:
            if self.room.checkPlayer(self.y, self.x + constants.gremlinWidth, constants.gremlinHeight, 2*self.range, singletons.hero):
                singletons.hero.hurt(self.att)
