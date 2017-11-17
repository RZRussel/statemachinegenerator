import unittest
from prism.generator import *
from prism.specification import *
import re

STUB_WORLD_MAPPINGS = {K_WORLD_MAX_X: 100, K_WORLD_MAX_Y: 100}
STUB_ISLAND_MAPPINGS = {K_ISLAND_CENTER_X: 50, K_ISLAND_CENTER_Y: 50, K_ISLAND_SMALL_RADIUS: 25,
                        K_ISLAND_BIG_RADIUS: 25}
STUB_PENGUIN_MAPPINGS = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                         K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
STUB_SNOWBALL_MAPPINGS = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}


class TestPenguinGenerator(unittest.TestCase):
    def test_moved(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                             STUB_SNOWBALL_MAPPINGS))
        label = "move"
        precondition_builder = ExpressionBuilder(Identifier("dead"))
        precondition_builder.append_not()

        #print(penguin_generator.moved(precondition_builder.expression, label))

    def test_island_collision(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))

        label = "collide"
        precondition_builder = ExpressionBuilder(Identifier(K_ISLAND_COLLISION))
        precondition_builder.append_not()

        print(penguin_generator.collide_island(precondition_builder.expression, label))