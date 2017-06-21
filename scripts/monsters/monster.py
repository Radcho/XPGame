import pyglet
from scripts import singletons, constants, projectile
from resources import resource_loader

class Monster(object):
    def __init__(self, x, y, room, sprite, width, height):
        self.hero = singletons.hero
        self.room = room
        self.x = x
        self.y = y

        self.health = 3

        self.invulnerability = 0

        self.width = width
        self.height = height

        self.sprite = pyglet.sprite.Sprite(sprite, x=self.x, y=self.y)

    def move(self):
        self.invulnerability = max(0, self.invulnerability - 1)

        if self.hero.attacking and self.invulnerability == 0:
            if self.y + self.height >= self.hero.y and self.y <= self.hero.y + constants.playerHeight:
                if (self.x <= self.hero.x + constants.playerWidth + self.hero.range and self.x + self.width >= self.hero.x + constants.playerWidth and self.hero.attacking == "right") or (self.x <= self.hero.x and self.x + self.width >= self.hero.x - self.hero.range and self.hero.attacking == "left"):
                    self.health -= self.hero.attackDamage
                    self.invulnerability = 30
            elif self.x <= self.hero.x + constants.playerWidth and self.x + self.width >= self.hero.x and self.hero.attacking == "up":
                if self.y <= self.hero.y + constants.playerHeight + self.hero.range and self.y + self.height >= self.hero.y + constants.playerHeight:
                    self.health -= self.hero.attackDamage
                    self.invulnerability = 30

        self.sprite.set_position(self.x, self.y)

        if self.health < 0:
            self.sprite.image = self.invisibleImage

    def attack(self):
        return
        print("waow")