from base_expression import *


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
        self.expression = BinaryOperation("&", self.expression, expression)

    def append_or(self, expression):
        self.expression = BinaryOperation("|", self.expression, expression)

    def append_not(self):
        self.expression = UnaryOperation("!", self.expression)

    def append_imply(self, expression):
        self.expression = BinaryOperation("->", self.expression, expression)

    def wrap_next(self):
        self.expression = Function("next", self.expression)

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

    def append_in(self, expression):
        self.expression = BinaryOperation("in", self.expression, expression)

    def build(self):
        return str(self.expression)
