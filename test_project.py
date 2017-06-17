from tests import hero_movement, monster_movement
import unittest

tests = []

## Hero movement tests
tests.append(unittest.defaultTestLoader.loadTestsFromTestCase(hero_movement.MovementTestCase))

## Monster movement tests
tests.append(unittest.defaultTestLoader.loadTestsFromTestCase(monster_movement.GhostTestCase))
tests.append(unittest.defaultTestLoader.loadTestsFromTestCase(monster_movement.GargoyleTestCase))
tests.append(unittest.defaultTestLoader.loadTestsFromTestCase(monster_movement.GremlinTestCase))
tests.append(unittest.defaultTestLoader.loadTestsFromTestCase(monster_movement.LichTestCase))
tests.append(unittest.defaultTestLoader.loadTestsFromTestCase(monster_movement.SkeletonTestCase))

runner = unittest.TextTestRunner()
for test in tests:
    runner.run(test)