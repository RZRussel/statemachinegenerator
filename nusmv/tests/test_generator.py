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

    def test_snowball_initialized(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 1, K_PENGUIN_SNOWBALL_OY: 2}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))

        assert penguin_generator.snowball_initialized() == """case
  next(snowball.direction) in 0..13 & (next(snowball.x) - x) = 1 & (next(snowball.y) - y) = 2 : TRUE;
  next(snowball.direction) in 14..39 & (next(snowball.x) - x) = 0 & (next(snowball.y) - y) = 2 : TRUE;
  next(snowball.direction) in 40..68 & (next(snowball.x) - x) = -1 & (next(snowball.y) - y) = 2 : TRUE;
  next(snowball.direction) in 69..74 & (next(snowball.x) - x) = -2 & (next(snowball.y) - y) = 2 : TRUE;
  next(snowball.direction) in 75..103 & (next(snowball.x) - x) = -2 & (next(snowball.y) - y) = 1 : TRUE;
  next(snowball.direction) in 104..129 & (next(snowball.x) - x) = -2 & (next(snowball.y) - y) = 0 : TRUE;
  next(snowball.direction) in 130..158 & (next(snowball.x) - x) = -2 & (next(snowball.y) - y) = -1 : TRUE;
  next(snowball.direction) in 159..164 & (next(snowball.x) - x) = -2 & (next(snowball.y) - y) = -2 : TRUE;
  next(snowball.direction) in 165..193 & (next(snowball.x) - x) = -1 & (next(snowball.y) - y) = -2 : TRUE;
  next(snowball.direction) in 194..219 & (next(snowball.x) - x) = 0 & (next(snowball.y) - y) = -2 : TRUE;
  next(snowball.direction) in 220..248 & (next(snowball.x) - x) = 1 & (next(snowball.y) - y) = -2 : TRUE;
  next(snowball.direction) in 249..254 & (next(snowball.x) - x) = 2 & (next(snowball.y) - y) = -2 : TRUE;
  next(snowball.direction) in 255..283 & (next(snowball.x) - x) = 2 & (next(snowball.y) - y) = -1 : TRUE;
  next(snowball.direction) in 284..309 & (next(snowball.x) - x) = 2 & (next(snowball.y) - y) = 0 : TRUE;
  next(snowball.direction) in 310..338 & (next(snowball.x) - x) = 2 & (next(snowball.y) - y) = 1 : TRUE;
  next(snowball.direction) in 339..344 & (next(snowball.x) - x) = 2 & (next(snowball.y) - y) = 2 : TRUE;
  next(snowball.direction) in 345..359 & (next(snowball.x) - x) = 1 & (next(snowball.y) - y) = 2 : TRUE;
  TRUE : FALSE;
esac;"""

    def test_flashed(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))

        assert penguin_generator.flashed() == """case
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

    def test_pushed(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 2,
                            K_PENGUIN_SLIDING_FRICTION: 1, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))

        assert penguin_generator.pushed() == """case
  pushed_velocity = 1 & pushed_index = 1 & direction in 0..30 & (next(x) - x) = 1 & (next(y) - y) = 0 : TRUE;
  pushed_velocity = 1 & pushed_index = 1 & direction in 31..60 & (next(x) - x) = 1 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 1 & pushed_index = 1 & direction in 61..120 & (next(x) - x) = 0 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 1 & pushed_index = 1 & direction in 121..149 & (next(x) - x) = -1 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 1 & pushed_index = 1 & direction in 150..209 & (next(x) - x) = -1 & (next(y) - y) = 0 : TRUE;
  pushed_velocity = 1 & pushed_index = 1 & direction in 210..240 & (next(x) - x) = -1 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 1 & pushed_index = 1 & direction in 241..300 & (next(x) - x) = 0 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 1 & pushed_index = 1 & direction in 301..330 & (next(x) - x) = 1 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 1 & pushed_index = 1 & direction in 331..359 & (next(x) - x) = 1 & (next(y) - y) = 0 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 0..30 & (next(x) - x) = 1 & (next(y) - y) = 0 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 31..60 & (next(x) - x) = 1 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 61..120 & (next(x) - x) = 0 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 121..149 & (next(x) - x) = -1 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 150..209 & (next(x) - x) = -1 & (next(y) - y) = 0 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 210..240 & (next(x) - x) = -1 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 241..300 & (next(x) - x) = 0 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 301..330 & (next(x) - x) = 1 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 2 & pushed_index = 1 & direction in 331..359 & (next(x) - x) = 1 & (next(y) - y) = 0 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 0..14 & (next(x) - x) = 2 & (next(y) - y) = 0 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 15..41 & (next(x) - x) = 2 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 42..48 & (next(x) - x) = 1 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 49..75 & (next(x) - x) = 1 & (next(y) - y) = 2 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 76..104 & (next(x) - x) = 0 & (next(y) - y) = 2 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 105..131 & (next(x) - x) = -1 & (next(y) - y) = 2 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 132..138 & (next(x) - x) = -1 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 139..165 & (next(x) - x) = -2 & (next(y) - y) = 1 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 166..194 & (next(x) - x) = -2 & (next(y) - y) = 0 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 195..221 & (next(x) - x) = -2 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 222..228 & (next(x) - x) = -1 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 229..255 & (next(x) - x) = -1 & (next(y) - y) = -2 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 256..284 & (next(x) - x) = 0 & (next(y) - y) = -2 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 285..311 & (next(x) - x) = 1 & (next(y) - y) = -2 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 312..318 & (next(x) - x) = 1 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 319..345 & (next(x) - x) = 2 & (next(y) - y) = -1 : TRUE;
  pushed_velocity = 2 & pushed_index = 2 & direction in 346..359 & (next(x) - x) = 2 & (next(y) - y) = 0 : TRUE;
  TRUE : FALSE;
esac;"""

    def test_pushed_initial_index(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 5, K_PENGUIN_FLASH_VELOCITY: 10,
                            K_PENGUIN_SLIDING_FRICTION: 1, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))

        assert penguin_generator.pushed_initial_index() == """case
  next(pushed_velocity) = 5 : 4;
  next(pushed_velocity) = 10 : 4;
  TRUE : 0;
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