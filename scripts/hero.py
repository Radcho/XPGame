import pyglet
from resources import resource_loader
from scripts import constants

class Hero(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.jumping = False

        self.room = None

        self.direction = {"left": False, "right": False}

        self.loadAnimations()

        self.walkSpeed = 4

        self.health = 12

        self.momx = 0
        self.momy = 0

    def loadAnimations(self):
        self.hero_idle = pyglet.image.load(resource_loader.files["player_idle.png"])
        self.hero_walking_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_right_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        self.hero_walking_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_left_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        self.animation = None
        self.heart_can = pyglet.image.load(resource_loader.files["heart_empty.png"])
        self.heart = [None if i == 0 else pyglet.image.load(resource_loader.files["heart_" + str(i) +".png"]) for i in range(5)]
        self.sprite = pyglet.sprite.Sprite(self.hero_idle)
        
        self.heart_batch = pyglet.graphics.Batch()
        self.heart_array = []
        for i in range(3):
            self.heart_array.append(pyglet.sprite.Sprite(self.heart_can, x=6+38*i, y=442, batch=self.heart_batch))

    def heartdraw(self):
        health = self.health
        for i in range(3):
            if health >= 4:
                pyglet.sprite.Sprite(self.heart[4], x=6+38*i, y=442).draw()
                health -= 4
            elif health > 0:
                pyglet.sprite.Sprite(self.heart[health], x=6+38*i, y=442).draw()
                break
    
    
    def setRoom(self, roomRef):
        self.room = roomRef

    def checkCollision(self):
        self.momy = max(self.momy - 1, -20)

        if self.room.checkMove(self.y + self.momy, self.x, constants.playerHeight, constants.playerWidth):
            self.momy //= 2
            if self.room.checkMove(self.y + self.momy, self.x, constants.playerHeight, constants.playerWidth):
                if self.momy < 0:
                    self.jumping = False
                self.momy = 0
        if self.room.checkMove(self.y, self.x + self.momx, constants.playerHeight, constants.playerWidth):
            self.momx //= 2
            if self.room.checkMove(self.y, self.x + self.momx, constants.playerHeight, constants.playerWidth):
                self.momx = 0
                self.health -= 1

        if self.room.checkMove(self.y + self.momy, self.x + self.momx, constants.playerHeight, constants.playerWidth):
            self.momy = 0

        self.x += self.momx
        self.y += self.momy
        
    def jump(self):
        if not self.jumping:
            self.momy = 13
            self.jumping = True

    def move(self, dt):
        animate = None
        if self.direction["left"]:
            animate = "left"
            self.momx = -self.walkSpeed
        elif self.direction["right"]:
            animate = "right"
            self.momx = self.walkSpeed
        else:
            self.momx = 0
        
        self.checkCollision()
        self.sprite.set_position(self.x, self.y)
        
        if animate and (not self.animation or self.animation != animate):
            self.animation = animate
            self.sprite.image = self.hero_walking_left if animate == "left" else self.hero_walking_right
        elif not animate and self.animation:
            self.animation = None
            self.sprite.image = self.hero_idle
