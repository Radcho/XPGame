import pyglet
import math
from scripts import singletons, constants
from scripts.monsters import monster
from resources import resource_loader

class Gremlin(monster.Monster):
    
    def __init__(self, x, y, room):
        self.gremlin_idle = pyglet.image.load(resource_loader.files["gremlin_idle.png"])
        self.gremlin_walking_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['gremlin_right_' + str(i) + '.png']) for i in range(1, 2)], 1/16)
        self.gremlin_walking_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['gremlin_left_' + str(i) + '.png']) for i in range(1, 2)], 1/16)

        super().__init__(x, y, room, self.gremlin_idle)

        self.fallSpeed = 0
        self.jumping = False

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

        self.sprite.set_position(self.x, self.y)
        self.sprite.image = self.gremlin_walking_left if self.direction == "left" else self.gremlin_walking_right

    def attack(self):
        return
        print("nerf this")
