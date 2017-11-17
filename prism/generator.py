from prism.expression_builder import *
from prism.specification import Specification
from generatortools import *
from physics import *
from typing import AnyStr, Any
from copy import deepcopy

K_PENGUIN_X = "x"
K_PENGUIN_Y = "y"
K_PENGUIN_DIRECTION = "direction"


class PenguinGenerator:
    MODULE_NAME = "Penguin"

    def __init__(self, specification: Specification):
        self._specification = specification

    @property
    def specification(self) -> Specification:
        return self._specification

    def moved(self, precondition: Any, label: AnyStr):
        move_offsets = radial_moves(self.specification.penguin.move_velocity)
        compacted_list = compact_list_by_index(move_offsets)

        guard_builder = GuardBuilder(label)

        for (x, y), direction in compacted_list:
            x_cond_builder = ExpressionBuilder(Identifier(K_PENGUIN_X))

            if x >= 0:
                x_cond_builder.append_add(Integer(x))

                update_builder = UpdateBuilder(Identifier(K_PENGUIN_X), x_cond_builder.expression)

                x_cond_builder.append_le(Integer(self._specification.world.max_x))
            else:
                x_cond_builder.append_subtract(Integer(-x))

                update_builder = UpdateBuilder(Identifier(K_PENGUIN_X), x_cond_builder.expression)

                x_cond_builder.append_ge(Integer(0))

            x_cond_builder.wrap_paranthesis()

            y_cond_builder = ExpressionBuilder(Identifier(K_PENGUIN_Y))
            if y >= 0:
                y_cond_builder.append_add(Integer(y))

                update_builder.add_update(Identifier(K_PENGUIN_Y), y_cond_builder.expression)

                y_cond_builder.append_le(Integer(self._specification.world.max_y))
            else:
                y_cond_builder.append_subtract(Integer(-y))

                update_builder.add_update(Identifier(K_PENGUIN_Y), y_cond_builder.expression)

                y_cond_builder.append_ge(Integer(0))

            y_cond_builder.wrap_paranthesis()

            if precondition is not None:
                condition_builder = ExpressionBuilder(precondition)
                condition_builder.append_and(x_cond_builder.expression)
            else:
                condition_builder = ExpressionBuilder(x_cond_builder.expression)

            condition_builder.append_and(y_cond_builder.expression)

            if type(direction) == range:
                for d in direction:
                    copy_update_builder = deepcopy(update_builder)
                    copy_update_builder.add_update(Identifier(K_PENGUIN_DIRECTION), d)
                    guard_builder.add_guard(condition_builder.expression, copy_update_builder.expression)
            else:
                update_builder.add_update(Identifier(K_PENGUIN_DIRECTION), direction)
                guard_builder.add_guard(condition_builder.expression, update_builder.expression)

        return guard_builder.build()
