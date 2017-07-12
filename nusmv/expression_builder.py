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

    def append_newline(self):
        self.expression = Newline(self.expression)

    def build(self):
        return str(self.expression)


class CaseBuilder:
    class Case:
        def __init__(self, condition, value):
            self.condition = condition
            self.value = value

        def __str__(self):
            return str(self.condition) + " : " + str(self.value)

    def __init__(self):
        self.cases = []

    def add_case(self, condition, value):
        self.cases.append(self.Case(condition, value))

    def and_with_cases(self, expression):
        self.cases = list(map(lambda case: self.__append_binary_operation("&", expression, case), self.cases))

    def merge(self, other):
        self.cases = self.cases + other.cases

    def build(self):
        flatten_cases = list(map(lambda case: str(case), self.cases))
        flatten_cases = list(map(lambda s: "  " + s + ";", flatten_cases))
        flatten_cases_str = "\n".join(flatten_cases)
        return "case\n" + flatten_cases_str + "\nesac"

    def __append_binary_operation(self, symbol, expression, case):
        return self.Case(BinaryOperation(symbol, expression, case.condition), case.value)
