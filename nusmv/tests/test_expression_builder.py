import unittest
from copy import deepcopy
from nusmv.expression import *
from nusmv.expression_builder import *
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

    def test_next(self):
        builder = ExpressionBuilder(Identifier("a"))
        builder.append_add(Identifier("b"))
        builder.wrap_next()

        assert builder.build() == "next(a + b)"

    def test_multiline_expression(self):
        builder = ExpressionBuilder(Identifier("x"))
        builder.append_imply(Identifier("y"))
        builder.append_newline()
        builder.append_or(Identifier("z"))

        assert builder.build() == "x -> y\n | z"


class TestCaseBuilder(unittest.TestCase):
    def test_with_in_condition(self):
        case_builder = CaseBuilder()

        expression_builder = ExpressionBuilder(Identifier("x"))
        expression_builder.append_in(Range(0, 10))

        case_builder.add_case(expression_builder.expression, Integer(10))
        case_builder.add_case(Bool.true(), Bool.false())

        assert case_builder.build() == "case\n  x in 0..10 : 10;\n  TRUE : FALSE;\nesac;"

    def test_and_append(self):
        case_builder = CaseBuilder()

        expression_builder = ExpressionBuilder(Identifier("x"))
        expression_builder.append_in(Range(0, 10))

        case_builder.add_case(expression_builder.expression, Integer(10))

        expression_builder = ExpressionBuilder(Identifier("y"))
        expression_builder.append_gt(Integer(0))

        case_builder.add_case(expression_builder.expression, Integer(0))
        case_builder.and_with_cases(BinaryOperation(">", Identifier("z"), Integer(0)))

        assert case_builder.build() == "case\n  z > 0 & x in 0..10 : 10;\n  z > 0 & y > 0 : 0;\nesac;"

    def test_merge(self):
        case_builder = CaseBuilder()

        expression_builder = ExpressionBuilder(Identifier("x"))
        expression_builder.append_in(Range(0, 10))

        case_builder.add_case(expression_builder.expression, Integer(10))

        expression_builder = ExpressionBuilder(Identifier("y"))
        expression_builder.append_gt(Integer(0))

        second_case_builder = CaseBuilder()
        second_case_builder.add_case(expression_builder.expression, Integer(0))

        case_builder.merge(second_case_builder)

        assert case_builder.build() == "case\n  x in 0..10 : 10;\n  y > 0 : 0;\nesac;"

    def test_empty(self):
        case_builder = CaseBuilder()
        assert case_builder.build() == "case\n\nesac;"
