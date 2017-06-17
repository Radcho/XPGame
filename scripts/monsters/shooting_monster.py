import pyglet
from scripts import singletons, constants, projectile
from scripts.monsters import monster

class ShootingMonster(monster.Monster):
    def __init__(self, x, y, room, sprite, projectile_anim, delay):
        super().__init__(x, y, room, sprite)

        self.projectiles = []
        self.projectile_anim = projectile_anim

        self.delay = delay

    def addProjectile(self, startX, startY, destinationX, destinationY, projectileSprite=None):
        if projectileSprite is None:
            projectileSprite = self.projectile_anim
        projectileToAdd = projectile.Projectile(startX, startY, destinationX, destinationY, self.room, projectileSprite)
        self.projectiles.append(projectileToAdd)
        pyglet.clock.schedule_interval(projectileToAdd.move, 1/30)

    def move(self):
        self.delay = max(self.delay - 1, 0)
        
        for projectile in self.projectiles:
            if not projectile.alive:
                pyglet.clock.unschedule(projectile.move)
                self.projectiles.remove(projectile)

        super().move()