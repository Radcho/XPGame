import pyglet, random
from scripts import singletons, constants, room
from resources import resource_loader

class Heart():
    def __init__(self, x, y, room):
        self.hero = singletons.hero
        self.room = room
        self.x = x
        self.y = y
        self.health = 1
        self.invulnerability = 0

        self.width = constants.heartWidth
        self.height = constants.heartHeight
        self.image = pyglet.image.load(resource_loader.files["heart.png"])
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x, y=self.y)

    def move(self, dt):
        if not self.room.checkMove(self.y - 1, self.x, self.height, self.width):
            self.y -= 1
            k = random.randint(0,2) - 1
            if not self.room.checkMove(self.y, self.x + k, self.height, self.width):
                self.x += k

        if self.room.checkPlayer(self.y, self.x, self.height, self.width, singletons.hero):
            self.hero.health += 2
            self.health = 0
        
        self.sprite.set_position(self.x, self.y)

