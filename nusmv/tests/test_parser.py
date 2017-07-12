import unittest
from nusmv.parser import *


class TestTemplateParser(unittest.TestCase):
    def test_with_two_tags(self):
        code = """MODULE Actor\n\tMoved = <moved>;\n\tFalled = <falled>;\n\tVAR\n\ta: int;'"""

        template = parse_template_from_string(code)

        assert template.code == code
        assert len(template.replacements) == 2
        assert template.replacements[0].module_name == "Actor"
        assert template.replacements[0].tag == "moved"
        assert template.replacements[0].origin == 22
        assert template.replacements[0].length == 7
        assert template.replacements[1].module_name == "Actor"
        assert template.replacements[1].tag == "falled"
        assert template.replacements[1].origin == 41
        assert template.replacements[1].length == 8

    def test_with_two_modules_two_tags(self):
        code = """MODULE Action\nMODULE Actor\n\tMoved = <moved>;\n\tFalled = <falled>;\n\tVAR\n\ta: int;'"""

        template = parse_template_from_string(code)

        assert template.code == code
        assert len(template.replacements) == 2
        assert template.replacements[0].module_name == "Actor"
        assert template.replacements[0].tag == "moved"
        assert template.replacements[0].origin == 36
        assert template.replacements[0].length == 7
        assert template.replacements[1].module_name == "Actor"
        assert template.replacements[1].tag == "falled"
        assert template.replacements[1].origin == 55
        assert template.replacements[1].length == 8

    def test_without_tags(self):
        code = """MODULE Actor\n\tVAR a: int;"""
        template = parse_template_from_string(code)

        assert template.code == code
        assert len(template.replacements) == 0


class TestModuleParser(unittest.TestCase):
    def test_with_two_modules(self):
        first_module = "MODULE Actor\n\tDEFINE\n\t\ta = 10;\n\tVAR\n\t\tb: int;\n\t\n"
        second_module = "MODULE Action\n\tVAR\n\tb: int;\n \n \t"
        code = first_module + second_module
        modules = parse_modules_from_string(code)

        assert len(modules) == 2
        assert modules[0].name == "Actor"
        assert modules[0].code == first_module
        assert modules[1].name == "Action"
        assert modules[1].code == second_module


class TestSpecificationParser(unittest.TestCase):
    def test_complicated_specification(self):
        yaml_string = """
        specification:

          world:
            # 736
            max_x: 736
            # 414
            max_y: 414

          island:
            # 368
            center_x: 368
            # 207
            center_y: 207
            # 162.5
            small_radius: 162
            # 251.5
            big_radius: 251

          penguin:
            # 27
            radius: 27
            # 5.4
            move_velocity: 5
            # 10
            flash_velocity: 10
            # 10
            snowball_ox: 10
            # 15
            snowball_oy: 15
            # 3.0
            sliding_friction: 3

          snowball:
            # 10
            radius: 10
            # 1.2
            fly_velocity: 10

          insertions:
            snowball_timer_max: 60
            pushing_index_max: 15
        """

        specification = parse_specification_from_string(yaml_string)

        assert specification.world.max_x == 736
        assert specification.world.max_y == 414
        assert specification.island.center_x == 368
        assert specification.island.center_y == 207
        assert specification.island.small_radius == 162
        assert specification.island.big_radius == 251
        assert specification.penguin.radius == 27
        assert specification.penguin.move_velocity == 5
        assert specification.penguin.flash_velocity == 10
        assert specification.penguin.snowball_ox == 10
        assert specification.penguin.snowball_oy == 15
        assert specification.snowball.radius == 10
        assert specification.snowball.fly_velocity == 10
        assert "snowball_timer_max" in specification.insertions
        assert "pushing_index_max" in specification.insertions
        assert "moved" not in specification.insertions
        assert specification.insertions["snowball_timer_max"] == 60
        assert specification.insertions["pushing_index_max"] == 15

    def test_empty_insertions(self):
        yaml_string = """
        specification:

          world:
            # 736
            max_x: 736
            # 414
            max_y: 414

          island:
            # 368
            center_x: 368
            # 207
            center_y: 207
            # 162.5
            small_radius: 162
            # 251.5
            big_radius: 251

          penguin:
            # 27
            radius: 27
            # 5.4
            move_velocity: 5
            # 10
            flash_velocity: 10
            # 10
            snowball_ox: 10
            # 15
            snowball_oy: 15
            # 3.0
            sliding_friction: 3

          snowball:
            # 10
            radius: 10
            # 1.2
            fly_velocity: 10
        """

        specification = parse_specification_from_string(yaml_string)

        assert specification.world.max_x == 736
        assert specification.world.max_y == 414
        assert specification.island.center_x == 368
        assert specification.island.center_y == 207
        assert specification.island.small_radius == 162
        assert specification.island.big_radius == 251
        assert specification.penguin.radius == 27
        assert specification.penguin.move_velocity == 5
        assert specification.penguin.flash_velocity == 10
        assert specification.penguin.snowball_ox == 10
        assert specification.penguin.snowball_oy == 15
        assert specification.snowball.radius == 10
        assert specification.snowball.fly_velocity == 10
        assert "snowball_timer_max" not in specification.insertions
        assert "pushing_index_max" not in specification.insertions
