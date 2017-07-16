import unittest
from nusmv.generator import *
from nusmv.specification import *
import re

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
        case_start = "case\\n"
        case_expr = """(  direction ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(x\\) - x\\) = -?[0-9]+ & \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, snowball_generator.flew()))

    def test_collision_detected(self):
        snowball_mappings = {K_SNOWBALL_RADIUS: 2, K_SNOWBALL_FLY_VELOCITY: 1}
        penguin_mappings = {K_PENGUIN_RADIUS: 2, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}

        snowball_generator = SnowballGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS,
                                                             penguin_mappings, snowball_mappings))
        case_start = "case\\n"
        case_expr = """(  \\(next\\(x\\) - next\\(owner\\.opponent\\.x\\)\\) = -?[0-9]+ \
& \\(next\\(y\\) - next\\(owner\\.opponent\\.y\\)\\) ((= -?[0-9]+)|(in -?[0-9]+\\.\\.-?[0-9]+)) : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, snowball_generator.collision_detected()))

    def test_dead_point_reached(self):
        snowball_mappings = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}
        island_mappings = {K_ISLAND_CENTER_X: 50, K_ISLAND_CENTER_Y: 50, K_ISLAND_SMALL_RADIUS: 2,
                           K_ISLAND_BIG_RADIUS: 2}
        snowball_generator = SnowballGenerator(Specification(STUB_WORLD_MAPPINGS, island_mappings,
                                                             STUB_PENGUIN_MAPPINGS, snowball_mappings))
        case_start = "case\\n"
        case_expr = """(  next\\(x\\) = [0-9]+ & next\\(y\\) ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, snowball_generator.dead_point_reached()))


class TestPenguinGenerator(unittest.TestCase):
    def test_moved(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                             STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  next\\(direction\\) ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(x\\) - x\\) = -?[0-9]+ & \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.moved()))

    def test_snowball_initialized(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 1, K_PENGUIN_SNOWBALL_OY: 2}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  next\\(snowball\\.direction\\) ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(snowball\\.x\\) - x\\) = -?[0-9]+ & \\(next\\(snowball\\.y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.snowball_initialized()))

    def test_flashed(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  direction ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(x\\) - x\\) = -?[0-9]+ & \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.flashed()))

    def test_collision_detected(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 2, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  \\(next\\(x\\) - next\\(opponent\\.x\\)\\) = -?[0-9]+ \
& \\(next\\(y\\) - next\\(opponent\\.y\\)\\) ((= -?[0-9]+)|(in -?[0-9]+\\.\\.-?[0-9]+)) : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.collision_detected()))

    def test_pushed(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 2,
                            K_PENGUIN_SLIDING_FRICTION: 1, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  pushed_velocity = [0-9]+ & pushed_index = [0-9]+ & \
direction ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) & \\(next\\(x\\) - x\\) = -?[0-9]+ \
& \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.pushed()))

    def test_pushed_initial_index(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 5, K_PENGUIN_FLASH_VELOCITY: 10,
                            K_PENGUIN_SLIDING_FRICTION: 1, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  next\\(pushed_velocity\\) = [0-9]+ : [0-9]+;\\n)*"""
        case_end = "  TRUE : 0;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.pushed_initial_index()))

    def test_max_pushed_index(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 5, K_PENGUIN_FLASH_VELOCITY: 10,
                            K_PENGUIN_SLIDING_FRICTION: 1, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))

        assert penguin_generator.max_pushed_index() == "4"

    def test_static_collision_initialized(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 2, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  \\(opponent\\.x - x\\) = -?[0-9]+ & \\(opponent\\.y - y\\) = -?[0-9]+ \
& next\\(direction\\) = [0-9]+ & next\\(pushed_velocity\\) = [0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.static_collision_initialized()))

    def test_flashing_collision(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 2, K_PENGUIN_MOVE_VELOCITY: 0, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  \\(opponent\\.x - x\\) = -?[0-9]+ & \\(opponent\\.y - y\\) = -?[0-9]+ \
& next\\(direction\\) = [0-9]+ & next\\(pushed_velocity\\) = [0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.flash_collision_initialized()))

    def test_dead_point_reached(self):
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 2,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        island_mappings = {K_ISLAND_CENTER_X: 50, K_ISLAND_CENTER_Y: 50, K_ISLAND_SMALL_RADIUS: 2,
                           K_ISLAND_BIG_RADIUS: 2}
        penguin_generator = PenguinGenerator(Specification(STUB_WORLD_MAPPINGS, island_mappings, penguin_mappings,
                                                           STUB_SNOWBALL_MAPPINGS))
        case_start = "case\\n"
        case_expr = """(  next\\(x\\) = [0-9]+ & next\\(y\\) ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        self.assertIsNotNone(re.match(result_expr, penguin_generator.dead_point_reached()))
