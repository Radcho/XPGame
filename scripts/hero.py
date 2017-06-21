import pyglet
from resources import resource_loader
from scripts import constants

class Hero(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.jumping = False
        self.attacking = None
        self.attackDelay = 0

        self.room = None

        self.direction = {"left": False, "right": False}

        self.loadAnimations()

        self.invulnerabilityLeft = 0

        self.walkSpeed = 4
        self.transition = None

        self.range = 30
        self.health = 12
        self.attackDamage = 1

        self.dead = False

        self.momx = 0
        self.momy = 0

    def loadAnimations(self):
        self.hero_idle = pyglet.image.load(resource_loader.files["player_idle.png"])
        self.hero_dead = pyglet.image.load(resource_loader.files["player_rip.png"])

        self.hero_walking_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_right_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        self.hero_walking_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_left_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        self.hero_attack_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_attack_right_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        self.hero_attack_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_attack_left_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        self.hero_attack_up = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['player_attack_up_' + str(i) + '.png']) for i in range(1, 9)], 1/16)
        
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

        if self.room.checkMove(self.y + self.momy, self.x + self.momx, constants.playerHeight, constants.playerWidth):
            self.momy = 0

        self.x += self.momx
        self.y += self.momy
        
    def jump(self):
        if not self.jumping:
            self.momy = 13
            self.jumping = True

    def hurt(self, amount, direction=None):
        if self.invulnerabilityLeft == 0:
            self.health = max(0, self.health - amount)
            self.invulnerabilityLeft = 30
            if self.health == 0:
                self.dead = True

    def attack(self):
        if self.attackDelay == 0:
            if self.direction["left"]:
                self.attacking = "left"
            elif self.direction["right"]:
                self.attacking = "right"
            else:
                self.attacking = "up"
            self.attackDelay = 30

    def move(self, dt):
        if self.dead:
            self.sprite.image = self.hero_dead
            return
        self.invulnerabilityLeft = max(0, self.invulnerabilityLeft - 1)
        self.attackDelay = max(0, self.attackDelay - 1)
        if self.attackDelay < 15:
            self.attacking = None
        if self.direction["left"]:
            self.momx = -self.walkSpeed
        elif self.direction["right"]:
            self.momx = self.walkSpeed
        else:
            self.momx = 0
        
        self.checkCollision()
        self.sprite.set_position(self.x, self.y)
        
        if not self.attacking:
            if self.sprite.image != self.hero_walking_left and self.direction["left"]:
                self.sprite.image = self.hero_walking_left
            elif self.sprite.image != self.hero_walking_right and self.direction["right"] and not self.direction["left"]:
                self.sprite.image = self.hero_walking_right
            elif not self.direction["left"] and not self.direction["right"]:
                self.sprite.image = self.hero_idle
        elif self.attacking:
            if self.sprite.image != self.hero_attack_left and self.attacking == "left":
                self.sprite.image = self.hero_attack_left
            elif self.sprite.image != self.hero_attack_right and self.attacking == "right":
                self.sprite.image = self.hero_attack_right
            elif self.sprite.image != self.hero_attack_up and self.attacking == "up":
                self.sprite.image = self.hero_attack_up

        if self.x <= 5:
            self.transition = "Left"
            self.x += self.walkSpeed
        elif self.x + constants.playerWidth >= constants.roomWidth-5:
            self.transition = "Right"
            self.x -= self.walkSpeed
        elif self.y <= 5:
            self.transition = "Down"
            self.y += 5
            self.momy = 10
        elif self.y + constants.playerHeight >= constants.roomHeight-5:
            self.transition = "Up"
            self.y -= 5
            self.momy = -2