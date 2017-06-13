import unittest
from scripts import hero, room, constants

class MovementTestCase(unittest.TestCase):
    def setUp(self):
        self.hero = hero.Hero()
        self.room = room.Room()
        self.hero.setRoom(self.room)

    def test_moveLeft(self):
        startX = self.hero.x
        self.hero.direction["left"] = True
        self.hero.move(None)
        self.assertTrue(self.hero.x < startX, "The hero didn't move left.")

    def test_moveRight(self):
        startX = self.hero.x
        self.hero.direction["right"] = True
        self.hero.move(None)
        self.assertTrue(self.hero.x > startX, "The hero didn't move right.")

    def test_jump(self):
        startY = self.hero.y
        self.hero.jump()
        self.assertTrue(self.hero.jumping, "The hero isn't jumping.")
        self.hero.move(None)
        self.assertTrue(self.hero.y > startY, "The hero didn't move.")

    def test_moveBothDirections(self):
        startX = self.hero.x
        self.hero.direction["left"] = True
        self.hero.direction["right"] = True
        self.hero.move(None)
        self.assertTrue(self.hero.x < startX, "The hero didn't move left.")

    def test_drop(self):
        startY = self.hero.y
        self.hero.move(None)
        self.assertTrue(self.hero.y < startY, "The hero didn't move.")

    def test_collisionLeft(self):
        self.hero.direction["left"] = True
        for i in range((constants.roomWidth // -self.hero.walkSpeed) + 1):
            self.hero.move(None)
        self.assertTrue(self.hero.x > 0, "The hero fell out.")

    def test_collisionRight(self):
        self.hero.direction["right"] = True
        for i in range((constants.roomWidth // self.hero.walkSpeed) + 1):
            self.hero.move(None)
        self.assertTrue(self.hero.x < constants.roomWidth, "The hero fell out.")

    def test_collisionTop(self):
        for i in range((constants.roomHeight // 13) + 1):
            self.hero.momy = 13
            self.hero.move(None)
        self.assertTrue(self.hero.y < constants.roomHeight)

    def test_collisionBottom(self):
        for i in range((constants.roomHeight) + 1):
            self.hero.move(None)
        self.assertTrue(self.hero.y > 0)