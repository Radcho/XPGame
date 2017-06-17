import pyglet
import math
from scripts import singletons, constants, projectile
from scripts.monsters import shooting_monster
from resources import resource_loader

class Skeleton(shooting_monster.ShootingMonster):
    
    def __init__(self, x, y, room):
        self.skeleton_idle = pyglet.image.load(resource_loader.files["player_idle.png"])
        self.skeleton_left = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['skeleton_left_' + str(i) + '.png']) for i in range(1, 2)], 1/16)
        self.skeleton_right = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['skeleton_right_' + str(i) + '.png']) for i in range(1, 2)], 1/16)
        
        super().__init__(x, y, room, self.skeleton_idle, None, 0)

        self.fallSpeed = 0
        self.jumping = False

        self.direction = "left"
        self.shootingDelay = 60
        self.attackDelay = -1
        self.attacking = False
        self.range = 8

        self.arrowGraphics = {}
        for i in [(1,1), (1,0), (0,1), (-1,0), (0,-1), (-1,-1), (1,-1), (-1,1)]:
            j = ["", "_right", "_left"][i[0]] + ["", "_up", "_down"][i[1]]
            self.arrowGraphics[i] = pyglet.image.load(resource_loader.files["arrow" + j + ".png"])
        
    def move(self, dt):

        def octant(kx, ky):
            return (self.hero.x - self.x)*kx < (self.hero.y - self.y)*ky
        
        self.fallSpeed -= 1
        endAttack = False
        if not self.attacking and not ((self.x <= self.hero.x + constants.playerWidth + self.range and self.hero.x <= self.x + constants.skeletonWidth + self.range) and abs(self.y - self.hero.y) < constants.tileHeight*3):
            self.shootingDelay -= 1
            if self.shootingDelay < 15:
                move = 0
                if self.shootingDelay == 0:
                    gx = 0
                    gy = 0
                    if octant(2, 1):
                        gx -= 1
                    if octant(-1, -2):
                        gy -= 1
                    if octant(-1,2):
                        gy += 1
                    if octant(-2,1):
                        gx +=1
                    self.addProjectile(self.x, self.y + (constants.skeletonHeight // 2), self.x + gx, self.y + (constants.skeletonHeight // 2) + gy, self.arrowGraphics[(gx, gy)])
                    self.shootingDelay = 60
                    endAttack = True
            else:
                self.direction = "right"
                move = 1
                if self.x >= self.hero.x:
                    move = -1
                    self.direction = "left"

            if self.room.checkMove(self.y, self.x + move, constants.skeletonHeight, constants.skeletonWidth):
                move = 0

        else:
            self.shootingDelay = 60
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
   
        if self.room.checkMove(self.y + self.fallSpeed, self.x, constants.skeletonHeight, constants.skeletonWidth):
            if self.fallSpeed < 0:
                self.jumping = False
            self.fallSpeed = 0

        if self.room.checkMove(self.y + self.fallSpeed, self.x + move, constants.skeletonHeight, constants.skeletonWidth):
            move = 0
        
        self.x += move
        self.y += self.fallSpeed
        
        if self.fallSpeed == 0 and move == 0 and not self.jumping and not self.attacking and not endAttack and not self.shootingDelay <= 30:
            self.jumping = True
            self.fallSpeed = 11

        self.sprite.image = self.skeleton_left if self.direction == "left" else self.skeleton_right
        super().move()

    def attack(self):
        return
        print("doot doot")
