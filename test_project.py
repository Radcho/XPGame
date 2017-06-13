from tests import hero_movement
import unittest

movementTests = unittest.defaultTestLoader.loadTestsFromTestCase(hero_movement.MovementTestCase)
runner = unittest.TextTestRunner()
runner.run(movementTests)