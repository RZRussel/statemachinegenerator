import unittest
from copy import deepcopy
from mcmas.expression import Bool
from mcmas.expression_builder import ExpressionBuilder, MultiAssignmentBuilder
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

        assert z_builder.build() == "!z and x"
        assert builder.build() == "((true and x or y) -> !z) and false"

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

    def test_multiline_expression(self):
        builder = ExpressionBuilder(Identifier("x"))
        builder.append_imply(Identifier("y"))
        builder.append_newline()
        builder.append_or(Identifier("z"))

        assert builder.build() == "x -> y\n or z"


class TestMultiAssignmentBuilder(unittest.TestCase):
    def test_with_one_item(self):
        builder = MultiAssignmentBuilder()

        expression_builder1 = ExpressionBuilder(Identifier("x"))
        expression_builder1.append_eq(Identifier("y"))

        expression_builder2 = ExpressionBuilder(Identifier("z"))
        expression_builder2.append_eq(Integer(10))

        builder.add_item(expression_builder1.expression, expression_builder2.expression)

        assert builder.build() == "x = y if z = 10;"

    def test_with_two_multi_items(self):
        builder = MultiAssignmentBuilder()

        expression_builder1 = ExpressionBuilder(Identifier("x"))
        expression_builder1.append_eq(Identifier("y"))

        expression_builder2 = ExpressionBuilder(Identifier("z"))
        expression_builder2.append_eq(Integer(10))

        combined_builder = ExpressionBuilder(expression_builder2.expression)
        combined_builder.wrap_paranthesis()
        combined_builder.append_and(expression_builder1.expression)

        builder.add_item(expression_builder1.expression, expression_builder2.expression)
        builder.add_item(combined_builder.expression, expression_builder1.expression)

        assert builder.build() == "x = y if z = 10;\n(z = 10) and x = y if x = y;"

    def test_merge(self):
        builder = MultiAssignmentBuilder()

        expression_builder1 = ExpressionBuilder(Identifier("x"))
        expression_builder1.append_eq(Identifier("y"))

        expression_builder2 = ExpressionBuilder(Identifier("z"))
        expression_builder2.append_eq(Integer(10))

        builder.add_item(expression_builder1.expression, expression_builder2.expression)

        expression_builder1 = ExpressionBuilder(Identifier("y"))
        expression_builder1.append_gt(Integer(0))

        expression_builder2 = ExpressionBuilder(Identifier("t"))
        expression_builder2.append_eq(Integer(14))

        second_builder = MultiAssignmentBuilder()
        second_builder.add_item(expression_builder1.expression, expression_builder2.expression)

        builder.merge(second_builder)

        assert builder.build() == "x = y if z = 10;\ny > 0 if t = 14;"

    def test_empty(self):
        builder = MultiAssignmentBuilder()
        assert builder.build() == ""
