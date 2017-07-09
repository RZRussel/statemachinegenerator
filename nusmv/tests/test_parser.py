import unittest
from nusmv.parser import *


class TestTemplateParser(unittest.TestCase):
    def test_with_two_tags(self):
        code = """MODULE Actor\n\tMoved = <moved>;\n\tFalled = <falled>;\n\tVAR\n\ta: int;'"""

        template = parse_template_from_string(code)

        assert template.code == code
        assert len(template.replacements) == 2
        assert template.replacements[0].tag == "moved"
        assert template.replacements[0].origin == 22
        assert template.replacements[0].length == 7
        assert template.replacements[1].tag == "falled"
        assert template.replacements[1].origin == 41
        assert template.replacements[1].length == 8

    def test_without_tags(self):
        code = """MODULE Actor\n\tVAR a: int;"""
        template = parse_template_from_string(code)

        assert template.code == code
        assert len(template.replacements) == 0


class TestTestCaseParser(unittest.TestCase):
    def test_with_two_modules(self):
        first_module = "MODULE Actor\n\tDEFINE\n\t\ta = 10;\n\tVAR\n\t\tb: int;"
        second_module = "MODULE Action\n\tVAR\n\tb: int;"
        code = first_module + "\n\t \n" + second_module + "\n \n \t"
        test_cases = parse_test_cases_from_string(code)

        assert len(test_cases) == 2;
        assert test_cases[0].code == first_module
        assert test_cases[1].code == second_module