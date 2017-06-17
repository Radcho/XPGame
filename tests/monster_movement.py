import unittest
from scripts import hero, room, constants, singletons
from scripts.monsters import ghost, gargoyle, gremlin, lich, skeleton

class GhostTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = singletons.hero
        self.room = room.Room()
        self.ghost = ghost.Ghost(100,100,self.room)
        self.hero.setRoom(self.room)

    def test_moveRight(self):
        self.ghost.x = self.hero.x - 200
        startX = self.ghost.x
        self.ghost.move(None)
        self.assertTrue(self.ghost.x > startX, "The ghost didn't move to the player on the right.")

    def test_moveLeft(self):
        self.ghost.x = self.hero.x + 200
        startX = self.ghost.x
        self.ghost.move(None)
        self.assertTrue(self.ghost.x < startX, "The ghost didn't move to the player on the left.")

    def test_moveUp(self):
        self.ghost.y = self.hero.y - 200
        startY = self.ghost.y
        self.ghost.move(None)
        self.assertTrue(self.ghost.y > startY, "The ghost didn't move to the player above.")

    def test_moveDown(self):
        self.ghost.y = self.hero.y + 200
        startY = self.ghost.y
        self.ghost.move(None)
        self.assertTrue(self.ghost.y < startY, "The ghost didn't move to the player below.")

    def test_startCharge(self):
        self.ghost.y = self.hero.y + 5
        self.ghost.x = self.hero.x + 5
        startCharge = self.ghost.charge
        self.ghost.move(None)
        self.assertTrue(self.ghost.charge > startCharge, "The ghost didn't prepare charging.")

    def test_endCharge(self):
        self.ghost.y = self.hero.y + 5
        self.ghost.x = self.hero.x + 5
        self.ghost.charge_duration = 0
        self.ghost.charge = 20
        self.ghost.move(None)
        self.assertTrue(self.ghost.charge_duration > 0, "The ghost didn't start charging.")

    def test_chargeDirectionAndDuration(self):
        self.ghost.charge_duration = 20
        self.ghost.charge_direction = (5,5)
        startX = self.ghost.x
        startY = self.ghost.y
        startDur = self.ghost.charge_duration
        self.ghost.move(None)
        self.assertTrue(self.ghost.charge_duration < startDur, "The ghost didn't end charging.")
        self.assertEqual(self.ghost.x, startX + 25, "The ghost didn't move the required ammount horizontaly.")
        self.assertEqual(self.ghost.y, startY + 25, "The ghost didn't move the required ammount verticaly.")

class GargoyleTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = singletons.hero
        self.room = room.Room()
        self.hero.setRoom(room)

    def test_gargoyleMovement(self):
        garg = gargoyle.Gargoyle(200, 200, self.room, "up")
        garg.move(None)
        self.assertTrue(garg.x == 200 and garg.y == 200, "The gargoyle... moved?")

    def test_gargoyleDirection(self):
        gargU = gargoyle.Gargoyle(200, 200, self.room, "up")
        self.assertEqual(gargU.direction, (0,1), "The gargoyle is not facing upwards.")
        gargD = gargoyle.Gargoyle(200, 200, self.room, "down")
        self.assertEqual(gargD.direction, (0,-1), "The gargoyle is not facing downwards.")
        gargL = gargoyle.Gargoyle(200, 200, self.room, "left")
        self.assertEqual(gargL.direction, (1,0), "The gargoyle is not facing leftwards.")
        gargR = gargoyle.Gargoyle(200, 200, self.room, "right")
        self.assertEqual(gargR.direction, (-1,0), "The gargoyle is not facing rightwards.")

    def test_gargoyleShooting(self):
        garg = gargoyle.Gargoyle(self.hero.x + 50, self.hero.y, self.room, "left")
        garg.delay = 0
        garg.move(None)
        self.assertGreater(garg.delay, 0, "The shooting delay wasn't reset.")
        self.assertTrue(len(garg.projectiles) > 0, "The projectile wasn't fired.")

    def test_gargoyleOppositeDirection(self):
        garg = garg = gargoyle.Gargoyle(self.hero.x + 50, self.hero.y, self.room, "right")
        garg.delay = 0
        garg.move(None)
        self.assertListEqual(garg.projectiles, [], "The gargoyle shot.")

class GremlinTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = singletons.hero
        self.room = room.Room()
        self.hero.setRoom(room)
        self.grem = gremlin.Gremlin(self.hero.x + 100, self.hero.y, self.room)

    def test_gremlinMoveLeft(self):
        startX = self.grem.x
        self.grem.move(None)
        self.assertEqual(self.grem.direction, "left", "The gremlin isn't looking to the left.")
        self.assertLess(self.grem.x, startX, "The gremlin didn't move left.")

    def test_gremlinMoveRight(self):
        self.grem.x = self.hero.x - 69
        startX = self.grem.x
        self.grem.move(None)
        self.assertEqual(self.grem.direction, "right", "The gremlin isn't looking to the right.")
        self.assertGreater(self.grem.x, startX, "The gremlin didn't move right.")

    def test_gremlinFalling(self):
        self.grem.y = 300
        startY = self.grem.y
        self.grem.move(None)
        self.assertLess(self.grem.y, startY, "The gremlin didn't fall.")

    def test_gremlinJumpOnObstacle(self):
        self.grem.x = 330
        self.grem.move(None)
        self.assertTrue(self.grem.jumping, "The gremlin didn't start jumping.")
        self.assertGreater(self.grem.fallSpeed, 0, "The gremlin isn't going up.")

class LichTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = singletons.hero
        self.room = room.Room()
        self.lich = lich.Lich(100,100,self.room)
        self.hero.setRoom(self.room)

    def test_moveTo(self):
        self.lich.x = self.hero.x + 150
        self.lich.y = self.hero.y + 149
        startX = self.lich.x
        startY = self.lich.y
        self.lich.move(None)
        self.assertLess(self.lich.x, startX, "The lich didn't move to the player horizontaly.")
        self.assertLess(self.lich.y, startY, "The lich didn't move to the player verticaly.")

    def test_moveAway(self):
        self.lich.x = self.hero.x + 20
        self.lich.y = self.hero.y + 20
        startX = self.lich.x
        startY = self.lich.y
        self.lich.move(None)
        self.assertGreater(self.lich.x, startX, "The lich didn't move away from the player horizontaly.")
        self.assertGreater(self.lich.y, startY, "The lich didn't move away from the player verticaly.")

    def test_stopMovement(self):
        self.lich.x = self.hero.x + 50
        self.lich.y = self.hero.y + 120
        startX = self.lich.x
        startY = self.lich.y
        self.lich.move(None)
        self.assertEqual(self.lich.x, startX, "The lich moved horizontaly.")
        self.assertEqual(self.lich.y, startY, "The lich moved verticaly.")

    def test_startCasting(self):
        self.lich.x = self.hero.x + 150
        self.lich.y = self.hero.y + 150
        self.lich.delay = 10
        startX = self.lich.x
        startY = self.lich.y
        self.lich.move(None)
        self.assertEqual(self.lich.x, startX, "The lich moved horizontaly.")
        self.assertEqual(self.lich.y, startY, "The lich moved verticaly.")

    def test_shoot(self):
        self.lich.delay = 0
        self.lich.move(None)
        self.assertGreater(self.lich.delay, 0, "The shooting delay wasn't reset.")
        self.assertTrue(len(self.lich.projectiles) > 0, "The projectile wasn't fired.")

class SkeletonTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = singletons.hero
        self.room = room.Room()
        self.hero.setRoom(room)
        self.skeltal = skeleton.Skeleton(self.hero.x + 100, self.hero.y, self.room)

    def test_skeletonMoveLeft(self):
        startX = self.skeltal.x
        self.skeltal.move(None)
        self.assertEqual(self.skeltal.direction, "left", "The skeleton isn't looking to the left.")
        self.assertLess(self.skeltal.x, startX, "The skeleton didn't move left.")

    def test_skeletonMoveRight(self):
        self.skeltal.x = self.hero.x - 69
        startX = self.skeltal.x
        self.skeltal.move(None)
        self.assertEqual(self.skeltal.direction, "right", "The skeleton isn't looking to the right.")
        self.assertGreater(self.skeltal.x, startX, "The skeleton didn't move right.")

    def test_skeletonFalling(self):
        self.skeltal.y = 300
        startY = self.skeltal.y
        self.skeltal.move(None)
        self.assertLess(self.skeltal.y, startY, "The skeleton didn't fall.")

    def test_skeletonJumpOnObstacle(self):
        self.skeltal.x = 330
        self.skeltal.move(None)
        self.assertTrue(self.skeltal.jumping, "The skeleton didn't start jumping.")
        self.assertGreater(self.skeltal.fallSpeed, 0, "The skeleton isn't going up.")

    def test_startShooting(self):
        self.skeltal.x = self.hero.x + 300
        self.skeltal.shootingDelay = 10
        startX = self.skeltal.x
        startY = self.skeltal.y
        self.skeltal.move(None)
        self.assertEqual(self.skeltal.x, startX, "The skeleton moved horizontaly.")
        self.assertEqual(self.skeltal.y, startY, "The skeleton moved verticaly.")

    def test_shoot(self):
        self.skeltal.x = self.hero.x + 300
        self.skeltal.shootingDelay = 1
        self.skeltal.move(None)
        self.assertGreater(self.skeltal.shootingDelay, 0, "The shooting delay wasn't reset.")
        self.assertTrue(len(self.skeltal.projectiles) > 0, "The projectile wasn't fired.")
        self.assertEqual(self.skeltal.projectiles[0].direction, (-1, 0), "The projectile flew in the wrong direction.")