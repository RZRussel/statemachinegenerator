import unittest
from nusmv.compiler import *
from nusmv.parser import *
from nusmv.generator import *
import re

STUB_WORLD_MAPPINGS = {K_WORLD_MAX_X: 100, K_WORLD_MAX_Y: 100}
STUB_ISLAND_MAPPINGS = {K_ISLAND_CENTER_X: 50, K_ISLAND_CENTER_Y: 50, K_ISLAND_SMALL_RADIUS: 25,
                        K_ISLAND_BIG_RADIUS: 25}
STUB_PENGUIN_MAPPINGS = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                         K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
STUB_SNOWBALL_MAPPINGS = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}


class TestCompiler(unittest.TestCase):
    def test_without_tags(self):
        specification = Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, STUB_PENGUIN_MAPPINGS,
                                      STUB_SNOWBALL_MAPPINGS)
        template_code = "MODULE Snowball\n  VAR\n  a: 0..10;\nMODULE Penguin\n VAR\n  b: 0..1;\n"
        template = parse_template_from_string(template_code)
        compiler = Compiler(template, specification, PenguinGenerator(specification), SnowballGenerator(specification))

        assert compiler.model_code == template_code
        assert compiler.compile() == template_code

    def test_undefined_tag(self):
        specification = Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, STUB_PENGUIN_MAPPINGS,
                                      STUB_SNOWBALL_MAPPINGS)

        template_code = """MODULE Snowball\n  DEFINE\nPos = @moved@;\n  VAR\n  a: 0..10;\n
        MODULE Penguin\n  DEFINE\nPos = @flew@;\n VAR\n  b: 0..1;\n"""

        template = parse_template_from_string(template_code)
        compiler = Compiler(template, specification, PenguinGenerator(specification), SnowballGenerator(specification))

        assert compiler.model_code == template_code
        assert compiler.compile() == template_code

    def test_with_two_tags(self):
        snowball_mappings = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        specification = Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                      snowball_mappings)

        template_code = """MODULE Snowball\n  DEFINE\nPos = @flew@;\n  VAR\n  a: 0..10;\n\
MODULE Penguin\n  DEFINE\nPos = @moved@;\n VAR\n  b: 0..1;\n"""

        template = parse_template_from_string(template_code)
        compiler = Compiler(template, specification, PenguinGenerator(specification), SnowballGenerator(specification))

        case_start = "case\\n"
        case_expr = """(  direction ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(x\\) - x\\) = -?[0-9]+ & \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        result = "MODULE Snowball\\n  DEFINE\\nPos = " + result_expr + ";\\n  VAR\n  a: 0\\.\\.10;\\n"

        case_start = "case\\n"
        case_expr = """(  next\\(direction\\) ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(x\\) - x\\) = -?[0-9]+ & \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        result = result + "MODULE Penguin\\n  DEFINE\\nPos = " + result_expr + ";\n VAR\n  b: 0\\.\\.1;\\n"
        self.assertIsNotNone(re.match(result, compiler.compile()))

    def test_with_two_tags_and_test_case(self):
        snowball_mappings = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        specification = Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                      snowball_mappings)

        template_code = """MODULE Snowball\n  DEFINE\nPos = @flew@;\n  VAR\n  a: 0..10;\n\
MODULE Penguin\n  DEFINE\nPos = @moved@;\n VAR\n  b: 0..1;\n"""

        template = parse_template_from_string(template_code)
        compiler = Compiler(template, specification, PenguinGenerator(specification), SnowballGenerator(specification))

        test_cases = parse_modules_from_string("""MODULE TestCase\n  VAR\n  p1: Penguin();\n""")

        case_start = "case\\n"
        case_expr = """(  direction ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(x\\) - x\\) = -?[0-9]+ & \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        result = "MODULE Snowball\\n  DEFINE\\nPos = " + result_expr + ";\n  VAR\n  a: 0\\.\\.10;\\n"

        case_start = "case\\n"
        case_expr = """(  next\\(direction\\) ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(x\\) - x\\) = -?[0-9]+ & \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        result = result + "MODULE Penguin\\n  DEFINE\\nPos = " + result_expr + ";\\n VAR\\n  b: 0\\.\\.1;\\n"

        test_case_expr = "MODULE TestCase\\n  VAR\\n  p1: Penguin\\(\\);\\n""" + "\\n\\n"
        main_code_expr = "MODULE main\\n  VAR\\n    test: TestCase;\\n"
        result = result + "\\n" + test_case_expr + main_code_expr

        self.assertIsNotNone(re.match(result, compiler.compile(test_cases[0])))

    def test_with_two_tags_test_case_and_insertion(self):
        snowball_mappings = {K_SNOWBALL_RADIUS: 10, K_SNOWBALL_FLY_VELOCITY: 1}
        penguin_mappings = {K_PENGUIN_RADIUS: 10, K_PENGUIN_MOVE_VELOCITY: 1, K_PENGUIN_FLASH_VELOCITY: 1,
                            K_PENGUIN_SLIDING_FRICTION: 3, K_PENGUIN_SNOWBALL_OX: 10, K_PENGUIN_SNOWBALL_OY: 15}
        specification = Specification(STUB_WORLD_MAPPINGS, STUB_ISLAND_MAPPINGS, penguin_mappings,
                                      snowball_mappings, {"Penguin.moved": "FALSE"})

        template_code = """MODULE Snowball\n  DEFINE\nPos = @flew@;\n  VAR\n  a: 0..10;
MODULE Penguin\n  DEFINE\nPos = @moved@;\n VAR\n  b: 0..1;\n"""

        template = parse_template_from_string(template_code)
        compiler = Compiler(template, specification, PenguinGenerator(specification), SnowballGenerator(specification))

        test_cases = parse_modules_from_string("""MODULE TestCase\n  VAR\n  p1: Penguin();\n""")

        case_start = "case\\n"
        case_expr = """(  direction ((= [0-9]+)|(in [0-9]+\\.\\.[0-9]+)) \
& \\(next\\(x\\) - x\\) = -?[0-9]+ & \\(next\\(y\\) - y\\) = -?[0-9]+ : TRUE;\\n)*"""
        case_end = "  TRUE : FALSE;\\nesac"
        result_expr = case_start + case_expr + case_end
        result = "MODULE Snowball\\n  DEFINE\\nPos = " + result_expr + ";\n  VAR\n  a: 0\\.\\.10;\\n"

        result = result + """MODULE Penguin\\n  DEFINE\\nPos = FALSE;\\n VAR\\n  b: 0\\.\\.1;\\n"""

        test_case_expr = "MODULE TestCase\\n  VAR\\n  p1: Penguin\\(\\);\\n""" + "\\n\\n"
        main_code_expr = "MODULE main\\n  VAR\\n    test: TestCase;\\n"
        result = result + "\\n" + test_case_expr + main_code_expr

        self.assertIsNotNone(re.match(result, compiler.compile(test_cases[0])))
