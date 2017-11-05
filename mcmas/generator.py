from mcmas.expression_builder import *
from generatortools import *
from physics import *

K_PENGUIN_X = "x"
K_PENGUIN_Y = "y"
K_PENGUIN_DIRECTION = "direction"


class PenguinGenerator:
    MODULE_NAME = "Penguin"

    def __init__(self, specification):
        self.specification = specification

    def moved(self):
        move_offsets = radial_moves(self.specification.penguin.move_velocity)
        compacted_list = compact_list_by_index(move_offsets)

        builder = MultiAssignmentBuilder()

        right_part_builder = ExpressionBuilder(Identifier("{}.Action".format(PenguinGenerator.MODULE_NAME)))
        right_part_builder.append_eq(Identifier("Move"))

        for (x, y), direction in compacted_list:
            x_expr = ExpressionBuilder(Identifier(K_PENGUIN_X))
            x_expr.append_subtract(Identifier(K_PENGUIN_X))
            x_expr.wrap_paranthesis()
            x_expr.append_eq(Integer(x))

            y_expr = ExpressionBuilder(Identifier(K_PENGUIN_Y))
            y_expr.append_subtract(Identifier(K_PENGUIN_Y))
            y_expr.wrap_paranthesis()
            y_expr.append_eq(Integer(y))

            d_expr = ExpressionBuilder(Identifier(K_PENGUIN_DIRECTION))

            if type(direction) == range:
                d_expr_copy = ExpressionBuilder(d_expr.expression)
                d_expr_copy.append_le(Integer(direction[-1]))
                d_expr_copy.wrap_paranthesis()
                d_expr.append_ge(Integer(direction[0]))
                d_expr.wrap_paranthesis()
                d_expr.append_and(d_expr_copy.expression)
            else:
                d_expr.append_eq(Integer(direction))

            d_expr.append_and(x_expr.expression)
            d_expr.append_and(y_expr.expression)

            builder.add_item(d_expr.expression, right_part_builder.expression)

        return builder.build()
