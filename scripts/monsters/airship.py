import pyglet
import math
from scripts import singletons, constants, projectile, bomb
from scripts.monsters import shooting_monster
from resources import resource_loader

class Airship(shooting_monster.ShootingMonster):
    
    def __init__(self, x, y, room):
        self.airship = pyglet.image.load(resource_loader.files['airship.png'])
        
        self.airship_bomb = pyglet.image.load(resource_loader.files['airship_bomb.png'])
        
        self.airship_skeler = pyglet.image.load(resource_loader.files['airship_skeleton_right.png'])
        self.airship_skelel = pyglet.image.load(resource_loader.files['airship_skeleton_left.png'])
        
        self.airship_gargr = pyglet.image.load(resource_loader.files['airship_garg_right.png'])
        self.airship_gargl = pyglet.image.load(resource_loader.files['airship_garg_left.png'])

        self.airship_lichr = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['airship_lich_right_' + str(i) + '.png']) for i in range(1, 2)], 1/16)
        self.airship_lichl = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['airship_lich_left_' + str(i) + '.png']) for i in range(1, 2)], 1/16)

        self.airship_lichr_gargr = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['airship_lich_right_with_gargoyle_right_' + str(i) + '.png']) for i in range(1, 2)], 1/16)
        self.airship_lichr_gargl = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['airship_lich_right_with_gargoyle_left_' + str(i) + '.png']) for i in range(1, 2)], 1/16)

        self.airship_lichl_gargr = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['airship_lich_left_with_gargoyle_right_' + str(i) + '.png']) for i in range(1, 2)], 1/16)
        self.airship_lichl_gargl = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['airship_lich_left_with_gargoyle_left_' + str(i) + '.png']) for i in range(1, 2)], 1/16)

        
        self.iceball_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['iceball_' + str(i) + '.png']) for i in range(1, 7)], 1/8)
        self.fireball_anim = pyglet.image.Animation.from_image_sequence([pyglet.image.load(resource_loader.files['fireball_' + str(i) + '.png']) for i in range(1, 7)], 1/8)
        self.arrowGraphic = [pyglet.image.load(resource_loader.files["arrow_left.png"]), pyglet.image.load(resource_loader.files["arrow_right.png"])]
        self.attack = 2
        self.ang = 0
        super().__init__(x, y, room, self.airship, constants.airshipWidth, constants.airshipHeight, self.iceball_anim, 720)
        self.health = 10
        
    def move(self, dt):        
        if self.delay == 0:
            self.delay = 720
        if self.delay % 90 == 10:
            self.addProjectile(self.x + 52, self.y + 44, self.hero.x, self.hero.y, self.attack)
        elif self.delay % 90 == 70:
            self.addProjectile(self.x + 110, self.y + 44, self.hero.x, self.hero.y, self.attack)

        if self.delay % 60 == 50:
            self.addProjectile(self.x + 143, self.y + 70, self.x + 144,  self.y + 70, self.attack, self.arrowGraphic[1])
        elif self.delay % 60 == 30:
            self.addProjectile(self.x, self.y + 70, self.x-5, self.y + 70, self.attack, self.arrowGraphic[0])
            
        elif self.delay % 80 == 0:
            self.addProjectile(self.x + 81, self.y + 8, self.x + 81, self.y, self.attack, self.fireball_anim)
        elif self.delay % 80 == 40:
            self.addProjectile(self.x + 64, self.y + 8, self.x + 64, self.y, self.attack, self.fireball_anim)

        elif self.delay % 180 == 130 or self.delay % 360 == 20 or self.delay % 360 == 220:
            self.addBomb()
            
        self.ang += math.pi/240          

        self.x += - math.cos(self.ang) * 1.5
        self.y += math.sin(self.ang) * 0.8


        if (self.delay - 10) % 90 < 10:
            if self.delay % 80 < 10 and self.sprite.image != self.airship_lichl_gargr:
                self.sprite.image = self.airship_lichl_gargr
            elif (self.delay - 40) % 80 < 10 and self.sprite.image != self.airship_lichl_gargl:
                self.sprite.image = self.airship_lichl_gargl
            elif self.delay % 80 >= 10 and (self.delay - 40) % 80 >= 10 and self.sprite.image != self.airship_lichl:
                self.sprite.image = self.airship_lichl
                
        elif (self.delay - 70) % 90 < 10:
            if self.delay % 80 < 10 and self.sprite.image != self.airship_lichr_gargr:
                self.sprite.image = self.airship_lichr_gargr
            elif (self.delay - 40) % 80 < 10 and self.sprite.image != self.airship_lichr_gargl:
                self.sprite.image = self.airship_lichr_gargl
            elif self.delay % 80 >= 10 and (self.delay - 40) % 80 >= 10 and self.sprite.image != self.airship_lichr:
                self.sprite.image = self.airship_lichr
                
        elif self.delay % 80 < 10:
            self.sprite.image = self.airship_gargr
        elif (self.delay - 40) % 80 < 10:
            self.sprite.image = self.airship_gargl
            
        elif (self.delay - 30) % 60 < 10:
            self.sprite.image = self.airship_skelel
        elif (self.delay - 50) % 60 < 10:
            self.sprite.image = self.airship_skeler
            
        elif (self.delay - 20) % 360 < 10 or (self.delay - 130) % 180 < 10 or (self.delay - 220) % 360 < 10:
            self.sprite.image = self.airship_bomb
            
        else:
            self.sprite.image = self.airship
        super().move()

    def addBomb(self):
        bombToAdd = bomb.Bomb(self.x + 105, self.y + 69, self.room, self.attack+1)
        self.projectiles.append(bombToAdd)
        pyglet.clock.schedule_interval(bombToAdd.move, 1/30)
