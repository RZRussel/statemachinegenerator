import unittest
from nusmv.model import *


class TestVerificationTemplate(unittest.TestCase):
    def test_add_replacement(self):
        template = VerificationTemplate("MODULE MyModule")

        replacement = Replacement("position", 0, 10)
        template.add_replacement(replacement)
        template.add_replacement(Replacement("velocity", 10, 15))

        assert len(template.replacements) == 2
        assert replacement in template.replacements

    def test_remove_replacement(self):
        template = VerificationTemplate("MODULE MyModule")

        replacement = Replacement("position", 0, 10)
        template.add_replacement(replacement)
        template.add_replacement(Replacement("velocity", 10, 15))
        template.remove_replacement(replacement)

        assert len(template.replacements) == 1
        assert replacement not in template.replacements

    def test_remove_all_replacements(self):
        template = VerificationTemplate("MODULE MyModule")

        replacement = Replacement("position", 0, 10)
        template.add_replacement(replacement)
        template.add_replacement(Replacement("velocity", 10, 15))

        template.remove_all_replacements()

        assert len(template.replacements) == 0
        assert replacement not in template.replacements


class TestTestCase(unittest.TestCase):
    def test_initialization(self):
        test_case = TestCase("MODULE MyModule")
        assert test_case.code == "MODULE MyModule"
