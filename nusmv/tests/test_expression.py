import unittest
from nusmv.expression import *
from base_expression import *


class TestStringifyExpression(unittest.TestCase):

    def test_range_expression(self):
        expression = Range(Integer(0), Integer(1))
        assert str(expression) == "0..1"

    def test_built_in_range(self):
        expression = Range.from_range(range(1,10))
        assert str(expression) == "1..9"
