import unittest
from nusmv.generator import *
from nusmv.specification import *

STUB_WORLD_MAPPINGS = {K_WORLD_MAX_X: 100, K_WORLD_MAX_Y: 100}
STUB_ISLAND_MAPPINGS = {K_ISLAND_CENTER_X: 50, K_ISLAND_CENTER_Y: 50, K_ISLAND_SMALL_RADIUS: 25,
                        K_ISLAND_BIG_RADIUS: 25}
STUB_PENGUIN_MAPPINGS = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                         K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
STUB_SNOWBALL_MAPPINGS = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}


class TestSnowballGenerator(unittest.TestCase):
    def test_flew(self):
        snowball_mappings = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}
        snowball_generator = SnowballGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS,
                                                             STUB_PENGUIN_MAPPINGS, snowball_mappings))

        assert snowball_generator.flew() == """case
  direction in 0..30 & (next(x) - x) = 1 & (next(y) - y) = 0 : TRUE;
  direction in 31..60 & (next(x) - x) = 1 & (next(y) - y) = 1 : TRUE;
  direction in 61..120 & (next(x) - x) = 0 & (next(y) - y) = 1 : TRUE;
  direction in 121..149 & (next(x) - x) = -1 & (next(y) - y) = 1 : TRUE;
  direction in 150..209 & (next(x) - x) = -1 & (next(y) - y) = 0 : TRUE;
  direction in 210..240 & (next(x) - x) = -1 & (next(y) - y) = -1 : TRUE;
  direction in 241..300 & (next(x) - x) = 0 & (next(y) - y) = -1 : TRUE;
  direction in 301..330 & (next(x) - x) = 1 & (next(y) - y) = -1 : TRUE;
  direction in 331..359 & (next(x) - x) = 1 & (next(y) - y) = 0 : TRUE;
  TRUE : FALSE;
esac;"""

    def test_collision_detected(self):
        snowball_mappings = {K_SNOWBALL_RADIUS: 2, K_SNOWBALL_FLY_VELOCITY: 1}
        penguin_mappings = {K_PENGUIN_RADIUS: 2, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}

        snowball_generator = SnowballGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS,
                                                             penguin_mappings, snowball_mappings))

        assert snowball_generator.collision_detected() == """case
  (next(x) - next(owner.opponent.x)) = -4 & (next(y) - next(owner.opponent.y)) = 0 : TRUE;
  (next(x) - next(owner.opponent.x)) = -3 & (next(y) - next(owner.opponent.y)) in -2..2 : TRUE;
  (next(x) - next(owner.opponent.x)) = -2 & (next(y) - next(owner.opponent.y)) in -3..3 : TRUE;
  (next(x) - next(owner.opponent.x)) = -1 & (next(y) - next(owner.opponent.y)) in -3..-2 : TRUE;
  (next(x) - next(owner.opponent.x)) = -1 & (next(y) - next(owner.opponent.y)) in 2..3 : TRUE;
  (next(x) - next(owner.opponent.x)) = 0 & (next(y) - next(owner.opponent.y)) in -4..-2 : TRUE;
  (next(x) - next(owner.opponent.x)) = 0 & (next(y) - next(owner.opponent.y)) in 2..4 : TRUE;
  (next(x) - next(owner.opponent.x)) = 1 & (next(y) - next(owner.opponent.y)) in -3..-2 : TRUE;
  (next(x) - next(owner.opponent.x)) = 1 & (next(y) - next(owner.opponent.y)) in 2..3 : TRUE;
  (next(x) - next(owner.opponent.x)) = 2 & (next(y) - next(owner.opponent.y)) in -3..3 : TRUE;
  (next(x) - next(owner.opponent.x)) = 3 & (next(y) - next(owner.opponent.y)) in -2..2 : TRUE;
  (next(x) - next(owner.opponent.x)) = 4 & (next(y) - next(owner.opponent.y)) = 0 : TRUE;
  TRUE : FALSE;
esac;"""

    def test_dead_point_reached(self):
        snowball_mappings = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}
        island_mappings = {K_ISLAND_CENTER_X: 50, K_ISLAND_CENTER_Y: 50, K_ISLAND_SMALL_RADIUS: 2,
                           K_ISLAND_BIG_RADIUS: 2}
        snowball_generator = SnowballGenerator(Specification(STUB_WORLD_MAPPINGS, island_mappings,
                                                             STUB_PENGUIN_MAPPINGS, snowball_mappings))

        assert snowball_generator.dead_point_reached() == """case
  next(x) = 47 & next(y) in 49..51 : TRUE;
  next(x) = 48 & next(y) in 48..49 : TRUE;
  next(x) = 48 & next(y) in 51..52 : TRUE;
  next(x) = 49 & next(y) in 47..48 : TRUE;
  next(x) = 49 & next(y) in 52..53 : TRUE;
  next(x) = 50 & next(y) = 47 : TRUE;
  next(x) = 50 & next(y) = 53 : TRUE;
  next(x) = 51 & next(y) in 47..48 : TRUE;
  next(x) = 51 & next(y) in 52..53 : TRUE;
  next(x) = 52 & next(y) in 48..49 : TRUE;
  next(x) = 52 & next(y) in 51..52 : TRUE;
  next(x) = 53 & next(y) in 49..51 : TRUE;
  TRUE : FALSE;
esac;"""


class TestPenguinGenerator(unittest.TestCase):
    def test_moved(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                             STUB_SNOWBALL_MAPPINGS))

        assert penguin_generator.moved() == """case
  next(direction) in 0..30 & (next(x) - x) = 1 & (next(y) - y) = 0 : TRUE;
  next(direction) in 31..60 & (next(x) - x) = 1 & (next(y) - y) = 1 : TRUE;
  next(direction) in 61..120 & (next(x) - x) = 0 & (next(y) - y) = 1 : TRUE;
  next(direction) in 121..149 & (next(x) - x) = -1 & (next(y) - y) = 1 : TRUE;
  next(direction) in 150..209 & (next(x) - x) = -1 & (next(y) - y) = 0 : TRUE;
  next(direction) in 210..240 & (next(x) - x) = -1 & (next(y) - y) = -1 : TRUE;
  next(direction) in 241..300 & (next(x) - x) = 0 & (next(y) - y) = -1 : TRUE;
  next(direction) in 301..330 & (next(x) - x) = 1 & (next(y) - y) = -1 : TRUE;
  next(direction) in 331..359 & (next(x) - x) = 1 & (next(y) - y) = 0 : TRUE;
  TRUE : FALSE;
esac;"""

    def test_collision_detected(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 2, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))

        assert penguin_generator.collision_detected() == """case
  (next(x) - next(opponent.x)) = -4 & (next(y) - next(opponent.y)) = 0 : TRUE;
  (next(x) - next(opponent.x)) = -3 & (next(y) - next(opponent.y)) in -2..2 : TRUE;
  (next(x) - next(opponent.x)) = -2 & (next(y) - next(opponent.y)) in -3..3 : TRUE;
  (next(x) - next(opponent.x)) = -1 & (next(y) - next(opponent.y)) in -3..-2 : TRUE;
  (next(x) - next(opponent.x)) = -1 & (next(y) - next(opponent.y)) in 2..3 : TRUE;
  (next(x) - next(opponent.x)) = 0 & (next(y) - next(opponent.y)) in -4..-2 : TRUE;
  (next(x) - next(opponent.x)) = 0 & (next(y) - next(opponent.y)) in 2..4 : TRUE;
  (next(x) - next(opponent.x)) = 1 & (next(y) - next(opponent.y)) in -3..-2 : TRUE;
  (next(x) - next(opponent.x)) = 1 & (next(y) - next(opponent.y)) in 2..3 : TRUE;
  (next(x) - next(opponent.x)) = 2 & (next(y) - next(opponent.y)) in -3..3 : TRUE;
  (next(x) - next(opponent.x)) = 3 & (next(y) - next(opponent.y)) in -2..2 : TRUE;
  (next(x) - next(opponent.x)) = 4 & (next(y) - next(opponent.y)) = 0 : TRUE;
  TRUE : FALSE;
esac;"""

    def test_dead_point_reached(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 2,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        island_mappings = {K_ISLAND_CENTER_X: 50, K_ISLAND_CENTER_Y: 50, K_ISLAND_SMALL_RADIUS: 2,
                           K_ISLAND_BIG_RADIUS: 2}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, island_mappings, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))

        assert penguin_generator.dead_point_reached() == """case
  next(x) = 46 & next(y) in 49..51 : TRUE;
  next(x) = 47 & next(y) in 48..52 : TRUE;
  next(x) = 48 & next(y) in 47..49 : TRUE;
  next(x) = 48 & next(y) in 51..53 : TRUE;
  next(x) = 49 & next(y) in 46..48 : TRUE;
  next(x) = 49 & next(y) in 52..54 : TRUE;
  next(x) = 50 & next(y) in 46..47 : TRUE;
  next(x) = 50 & next(y) in 53..54 : TRUE;
  next(x) = 51 & next(y) in 46..48 : TRUE;
  next(x) = 51 & next(y) in 52..54 : TRUE;
  next(x) = 52 & next(y) in 47..49 : TRUE;
  next(x) = 52 & next(y) in 51..53 : TRUE;
  next(x) = 53 & next(y) in 48..52 : TRUE;
  next(x) = 54 & next(y) in 49..51 : TRUE;
  TRUE : FALSE;
esac;"""