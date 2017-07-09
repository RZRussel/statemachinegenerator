import unittest
from copy import deepcopy
from nusmv.expression import *
from nusmv.expression_builder import *
from base_expression import *


class TestExpressionBuilder(unittest.TestCase):
    def test_ariphmetic_expression(self):
        self.builder = ExpressionBuilder(Identifier("a"))
        self.builder.append_add(Identifier("b"))
        self.builder.append_subtract(Identifier("c"))
        self.builder.wrap_paranthesis()
        self.builder.append_multiply(Integer(77))
        self.builder.append_divide(Identifier("d"))

        assert self.builder.build() == "(a + b - c) * 77 / d"

    def test_logic_expression_with_deep_copy(self):
        builder = ExpressionBuilder(Bool.true())
        builder.append_and(Identifier("x"))
        builder.append_or(Identifier("y"))
        builder.wrap_paranthesis()

        z_builder = ExpressionBuilder(Identifier("z"))
        z_builder.append_not()

        builder.append_imply(deepcopy(z_builder.expression))
        builder.wrap_paranthesis()
        builder.append_and(Bool.false())

        z_builder.append_and("x")

        assert z_builder.build() == "!z & x"
        assert builder.build() == "((TRUE & x | y) -> !z) & FALSE"

    def test_range_expression(self):
        builder = ExpressionBuilder(Integer(5))
        builder.append_in(Range(0, 10))

        assert builder.build() == "5 in 0..10"

    def test_comparison_expression(self):
        builder = ExpressionBuilder(Identifier("a"))
        builder.append_eq(Identifier("b"))
        builder.wrap_paranthesis()
        builder.append_lt(Identifier("c"))
        builder.append_gt(Identifier("d"))
        builder.wrap_paranthesis()
        builder.append_le(Identifier("a"))
        builder.append_ge(Identifier("b"))

        assert builder.build() == "((a = b) < c > d) <= a >= b"
