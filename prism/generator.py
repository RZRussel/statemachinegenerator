from prism.expression_builder import *
import prism.expression
from prism.specification import Specification
from generatortools import *
from physics import *
from typing import AnyStr, Any
from copy import deepcopy

K_PENGUIN_X = "x"
K_PENGUIN_Y = "y"
K_PENGUIN_DIRECTION = "direction"
K_ISLAND_COLLISION = "i_col"

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

    def collide_island(self, precondition: Any, label: AnyStr):
        center = (self.specification.island.center_x, self.specification.island.center_y)
        a = self.specification.island.small_radius
        b = self.specification.island.big_radius

        move_dead_points = reachable_points_from_ellipsis(center, a, b, self.specification.penguin.move_velocity)
        flash_dead_points = reachable_points_from_ellipsis(center, a, b, self.specification.penguin.flash_velocity)
        compacted_points = compact_2d_points(list(move_dead_points.union(flash_dead_points)))

        guard_builder = GuardBuilder(label)

        or_builder = None
        for x, y in compacted_points:
            x_expr = ExpressionBuilder(K_PENGUIN_X)
            x_expr.append_eq(Integer(x))

            y_expr = ExpressionBuilder(K_PENGUIN_Y)

            if type(y) == range:
                copy_y_expr = deepcopy(y_expr)
                y_expr.append_ge(y[0])
                copy_y_expr.append_le(y[-1])
                y_expr.append_and(copy_y_expr.expression)
            else:
                y_expr.append_eq(Integer(y))

            x_expr.append_and(y_expr.expression)
            x_expr.append_newline()

            if or_builder is None:
                or_builder = ExpressionBuilder(x_expr.expression)
            else:
                or_builder.append_or(x_expr.expression)

        or_builder.wrap_paranthesis()

        if precondition is None:
            condition_builder = ExpressionBuilder(or_builder.expression)
        else:
            condition_builder = ExpressionBuilder(precondition)
            condition_builder.append_and(or_builder.expression)

        update_builder = UpdateBuilder(Identifier(K_ISLAND_COLLISION), prism.expression.Bool(True))
        guard_builder.add_guard(condition_builder.expression, update_builder.expression)

        return guard_builder.build()
