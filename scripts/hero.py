import pyglet
from resources import resource_loader
from scripts import constants, functions

class Hero(object):
    
    def __init__(self):
        self.x = 100
        self.y = 280

        self.jumping = False

        self.currentRoom = None

        self.direction = {"up": False, "down": False, "left": False, "right": False}

        self.loadAnimations()

        self.walkSpeed = 4

        self.momx = 0
        self.momy = 0

    def loadAnimations(self):
        self.hero_idle = pyglet.image.load(resource_loader.files["player_idle.png"])
        self.hero_walking_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_right_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        self.hero_walking_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_left_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        self.animation = None
        self.sprite = pyglet.sprite.Sprite(self.hero_idle)

    def setRoom(self, roomRef):
        self.currentRoom = roomRef

    def checkCollision(self):
        self.momy -= 1

        if functions.checkMove(self.y + self.momy, self.x, constants.playerHeight, constants.playerWidth, self.currentRoom):
            if self.momy < 0:
                self.jumping = False
            self.momy = 0
        if functions.checkMove(self.y, self.x + self.momx, constants.playerHeight, constants.playerWidth, self.currentRoom):
            self.momx = 0

        if functions.checkMove(self.y + self.momy, self.x + self.momx, constants.playerHeight, constants.playerWidth, self.currentRoom):
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
