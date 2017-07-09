import unittest
from base_expression import *


class TestStringifyExpression(unittest.TestCase):
    def test_integer(self):
        expression = Integer(77)
        assert str(expression) == "77"

    def test_identifier(self):
        expression = Identifier("77")
        assert str(expression) == "77"

    def test_unary_operation(self):
        expression = UnaryOperation("-", Integer(77))
        assert str(expression) == "-77"

    def test_binary_operation(self):
        expression = BinaryOperation("+", Identifier("a"), Integer(77))
        assert str(expression) == "a + 77"

    def test_function_without_arguments(self):
        expression = Function("func")
        assert str(expression) == "func()"

    def test_function_one_argument(self):
        expression = Function("func", Identifier("a"))
        assert str(expression) == "func(a)"

    def test_function_three_argument(self):
        expression = Function("func", Identifier("a"), Identifier("b"), Integer(77))
        assert str(expression) == "func(a, b, 77)"

    def test_paranthesis(self):
        expression = Paranthesis(BinaryOperation("*", Identifier("a"), Identifier("b")))
        assert str(expression) == "(a * b)"