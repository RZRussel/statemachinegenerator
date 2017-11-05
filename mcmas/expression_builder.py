from base_expression import *
from typing import Any
from copy import deepcopy


class ExpressionBuilder:
    def __init__(self, expression):
        self.expression = expression

    def append_add(self, expression):
        self.expression = BinaryOperation("+", self.expression, expression)

    def append_subtract(self, expression):
        self.expression = BinaryOperation("-", self.expression, expression)

    def append_multiply(self, expression):
        self.expression = BinaryOperation("*", self.expression, expression)

    def append_divide(self, expression):
        self.expression = BinaryOperation("/", self.expression, expression)

    def append_negate(self):
        self.expression = UnaryOperation("-", self.expression)

    def append_and(self, expression):
        self.expression = BinaryOperation("and", self.expression, expression)

    def append_or(self, expression):
        self.expression = BinaryOperation("or", self.expression, expression)

    def append_not(self):
        self.expression = UnaryOperation("!", self.expression)

    def append_imply(self, expression):
        self.expression = BinaryOperation("->", self.expression, expression)

    def wrap_paranthesis(self):
        self.expression = Paranthesis(self.expression)

    def append_eq(self, expression):
        self.expression = BinaryOperation("=", self.expression, expression)

    def append_lt(self, expression):
        self.expression = BinaryOperation("<", self.expression, expression)

    def append_le(self, expression):
        self.expression = BinaryOperation("<=", self.expression, expression)

    def append_gt(self, expression):
        self.expression = BinaryOperation(">", self.expression, expression)

    def append_ge(self, expression):
        self.expression = BinaryOperation(">=", self.expression, expression)

    def append_newline(self):
        self.expression = Newline(self.expression)

    def build(self):
        return str(self.expression)


class MultiAssignmentBuilder:
    class MultiAssignmentItem:
        def __init__(self, lhs: Any, rhs: Any):
            self._lhs = lhs
            self._rhs = rhs

        def __str__(self):
            return "{} if {};".format(str(self._lhs), str(self._rhs))

    def __init__(self):
        self._items = []

    @property
    def items(self) -> list:
        return self._items

    def add_item(self, lhs: Any, rhs: Any):
        self._items.append(MultiAssignmentBuilder.MultiAssignmentItem(lhs, rhs))

    def merge(self, other):
        self._items = self._items + deepcopy(other.items)

    def build(self) -> str:
        result = ""

        for i in range(0, len(self._items)):
            if i == 0:
                result = "{}".format(str(self._items[i]))
            else:
                result = "{}\n{}".format(result, str(self._items[i]))

        return result
