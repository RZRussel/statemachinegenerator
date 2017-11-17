import unittest
from copy import deepcopy
from prism.expression import *
from prism.expression_builder import *
from base_expression import *


class TestExpressionBuilder(unittest.TestCase):
    def test_ariphmetic_expression(self):
        builder = ExpressionBuilder(Identifier("a"))
        builder.append_add(Identifier("b"))
        builder.append_subtract(Identifier("c"))
        builder.wrap_paranthesis()
        builder.append_multiply(Integer(77))
        builder.append_divide(Identifier("d"))

        assert builder.build() == "(a + b - c) * 77 / d"

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
        assert builder.build() == "((true & x | y) -> !z) & false"

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

    def test_next(self):
        builder = ExpressionBuilder(Identifier("a"))
        builder.append_add(Identifier("b"))
        builder.wrap_paranthesis()
        builder.wrap_next()

        assert builder.build() == "(a + b)\'"

    def test_multiline_expression(self):
        builder = ExpressionBuilder(Identifier("x"))
        builder.append_imply(Identifier("y"))
        builder.append_newline()
        builder.append_or(Identifier("z"))

        assert builder.build() == "x -> y\n | z"


class TestGuardBuilder(unittest.TestCase):
    def test_simple_guard(self):
        guard_builder = GuardBuilder("move")

        expression_builder = ExpressionBuilder(Identifier("x"))
        expression_builder.append_ge(Integer(7))

        update_builder = UpdateBuilder(Identifier("x"), Identifier("y"))

        guard_builder.add_guard(expression_builder.expression, update_builder.expression)

        self.assertEqual(guard_builder.build(), "[move] x >= 7 -> (x' = y);")

    def test_multi_update_guard(self):
        guard_builder = GuardBuilder("move")

        expression_builder = ExpressionBuilder(Identifier("x"))
        expression_builder.append_lt(Identifier("y"))

        value_builder = ExpressionBuilder(Identifier("z"))
        value_builder.append_add(Integer(7))

        update_builder = UpdateBuilder(Identifier("x"), value_builder.expression)

        value_builder = ExpressionBuilder(Identifier("y"))
        value_builder.append_multiply(Identifier("z"))

        update_builder.add_update(Identifier("y"), value_builder.expression)

        guard_builder.add_guard(expression_builder.expression, update_builder.expression)

        self.assertEqual(guard_builder.build(), "[move] x < y -> (x' = z + 7) & (y' = y * z);")

    def test_multi_guard(self):
        guard_builder = GuardBuilder("")

        expression_builder = ExpressionBuilder(Identifier("x"))
        expression_builder.append_lt(Identifier("y"))

        value_builder = ExpressionBuilder(Identifier("z"))
        value_builder.append_add(Integer(7))

        update_builder = UpdateBuilder(Identifier("x"), value_builder.expression)

        value_builder = ExpressionBuilder(Identifier("y"))
        value_builder.append_multiply(Identifier("z"))

        update_builder.add_update(Identifier("y"), value_builder.expression)

        guard_builder.add_guard(expression_builder.expression, update_builder.expression)
        guard_builder.add_guard(expression_builder.expression, update_builder.expression)

        self.assertEqual(guard_builder.build(), "[] x < y -> (x' = z + 7) & (y' = y * z);\n\
[] x < y -> (x' = z + 7) & (y' = y * z);")