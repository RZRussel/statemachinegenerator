from nusmv.expression_builder import *
from nusmv.expression import *
from generatortools import *
from physics import *

K_PENGUIN_X = "x"
K_PENGUIN_Y = "y"
K_PENGUIN_DIRECTION = "direction"
K_PENGUIN_SNOWBALL = "snowball"

K_SNOWBALL_X = "x"
K_SNOWBALL_Y = "y"
K_SNOWBALL_DIRECTION = "direction"

K_SNOWBALL_OTHER_PENGUIN = "owner.opponent"
K_PENGUIN_OTHER_PENGUIN = "opponent"


class SnowballGenerator:
    def __init__(self, specification):
        self.specification = specification

    def flew(self):
        fly_offsets = radial_moves(self.specification.snowball.fly_velocity)
        compacted_list = compact_list_by_index(fly_offsets)

        case_builder = CaseBuilder()

        for point, direction in compacted_list:
            x_expr = ExpressionBuilder(Identifier(K_SNOWBALL_X))
            x_expr.wrap_next()
            x_expr.append_subtract(Identifier(K_SNOWBALL_X))
            x_expr.wrap_paranthesis()
            x_expr.append_eq(Integer(point[0]))

            y_expr = ExpressionBuilder(Identifier(K_SNOWBALL_Y))
            y_expr.wrap_next()
            y_expr.append_subtract(Identifier(K_SNOWBALL_Y))
            y_expr.wrap_paranthesis()
            y_expr.append_eq(Integer(point[1]))

            d_expr = ExpressionBuilder(Identifier(K_SNOWBALL_DIRECTION))

            if type(direction) == range:
                d_expr.append_in(Range.from_range(direction))
            else:
                d_expr.append_eq(Integer(direction))

            d_expr.append_and(x_expr.expression)
            d_expr.append_and(y_expr.expression)

            case_builder.add_case(d_expr.expression, Bool.true())

        case_builder.add_case(Bool.true(), Bool.false())

        return case_builder.build()

    def collision_detected(self):
        src_radius = self.specification.penguin.radius
        src_velocity = self.specification.penguin.flash_velocity
        dst_radius = self.specification.snowball.radius
        dst_velocity = self.specification.snowball.fly_velocity

        offsets = collision_offsets_for_circle_bodies(src_radius, src_velocity, dst_radius, dst_velocity)
        compacted_offsets = compact_2d_points(offsets)

        builder = CaseBuilder()

        for x, y in compacted_offsets:
            opponent_x_expr = ExpressionBuilder(Identifier(K_SNOWBALL_OTHER_PENGUIN+"."+K_PENGUIN_X))
            opponent_x_expr.wrap_next()

            x_expr = ExpressionBuilder(Identifier(K_SNOWBALL_X))
            x_expr.wrap_next()
            x_expr.append_subtract(opponent_x_expr.expression)
            x_expr.wrap_paranthesis()
            x_expr.append_eq(Integer(x))

            opponent_y_expr = ExpressionBuilder(Identifier(K_SNOWBALL_OTHER_PENGUIN+"."+K_PENGUIN_Y))
            opponent_y_expr.wrap_next()

            y_expr = ExpressionBuilder(Identifier(K_SNOWBALL_Y))
            y_expr.wrap_next()
            y_expr.append_subtract(opponent_y_expr.expression)
            y_expr.wrap_paranthesis()

            if type(y) == range:
                y_expr.append_in(Range.from_range(y))
            else:
                y_expr.append_eq(y)

            x_expr.append_and(y_expr.expression)

            builder.add_case(x_expr.expression, Bool.true())

        builder.add_case(Bool.true(), Bool.false())

        return builder.build()

    def dead_point_reached(self):
        center = (self.specification.island.center_x, self.specification.island.center_y)
        a = self.specification.island.small_radius
        b = self.specification.island.big_radius
        velocity = self.specification.snowball.fly_velocity

        dead_points = reachable_points_from_ellipsis(center, a, b, velocity)
        compacted_points = compact_2d_points(list(dead_points))

        builder = CaseBuilder()

        for x, y in compacted_points:
            x_expr = ExpressionBuilder(K_SNOWBALL_X)
            x_expr.wrap_next()
            x_expr.append_eq(Integer(x))

            y_expr = ExpressionBuilder(K_SNOWBALL_Y)
            y_expr.wrap_next()

            if type(y) == range:
                y_expr.append_in(Range.from_range(y))
            else:
                y_expr.append_eq(y)

            x_expr.append_and(y_expr.expression)
            builder.add_case(x_expr.expression, Bool.true())

        builder.add_case(Bool.true(), Bool.false())

        return builder.build()


class PenguinGenerator:
    def __init__(self, specification):
        self.specification = specification

    def moved(self):
        move_offsets = radial_moves(self.specification.penguin.move_velocity)
        compacted_list = compact_list_by_index(move_offsets)

        case_builder = CaseBuilder()

        for point, direction in compacted_list:
            x_expr = ExpressionBuilder(Identifier(K_PENGUIN_X))
            x_expr.wrap_next()
            x_expr.append_subtract(Identifier(K_PENGUIN_X))
            x_expr.wrap_paranthesis()
            x_expr.append_eq(Integer(point[0]))

            y_expr = ExpressionBuilder(Identifier(K_PENGUIN_Y))
            y_expr.wrap_next()
            y_expr.append_subtract(Identifier(K_PENGUIN_Y))
            y_expr.wrap_paranthesis()
            y_expr.append_eq(Integer(point[1]))

            d_expr = ExpressionBuilder(Identifier(K_PENGUIN_DIRECTION))
            d_expr.wrap_next()

            if type(direction) == range:
                d_expr.append_in(Range.from_range(direction))
            else:
                d_expr.append_eq(Integer(direction))

            d_expr.append_and(x_expr.expression)
            d_expr.append_and(y_expr.expression)

            case_builder.add_case(d_expr.expression, Bool.true())

        case_builder.add_case(Bool.true(), Bool.false())

        return case_builder.build()

    def snowball_initialized(self):
        snowball_offsets = rotate_position((self.specification.penguin.snowball_ox,
                                            self.specification.penguin.snowball_oy))

        compacted_offsets = compact_list_by_index(snowball_offsets)

        builder = CaseBuilder()

        for offset, direction in compacted_offsets:
            x_expr = ExpressionBuilder(Identifier(K_PENGUIN_SNOWBALL + "." + K_SNOWBALL_X))
            x_expr.wrap_next()
            x_expr.append_subtract(Identifier(K_PENGUIN_X))
            x_expr.wrap_paranthesis()
            x_expr.append_eq(offset[0])

            y_expr = ExpressionBuilder(Identifier(K_PENGUIN_SNOWBALL + "." + K_SNOWBALL_Y))
            y_expr.wrap_next()
            y_expr.append_subtract(Identifier(K_PENGUIN_Y))
            y_expr.wrap_paranthesis()
            y_expr.append_eq(offset[1])

            direction_expr = ExpressionBuilder(Identifier(K_PENGUIN_SNOWBALL + "." + K_SNOWBALL_DIRECTION))
            direction_expr.wrap_next()

            if type(direction) == range:
                direction_expr.append_in(Range.from_range(direction))
            else:
                direction_expr.append_eq(direction)

            direction_expr.append_and(x_expr.expression)
            direction_expr.append_and(y_expr.expression)

            builder.add_case(direction_expr.expression, Bool.true())

        builder.add_case(Bool.true(), Bool.false())

        return builder.build()

    def flashed(self):
        pass

    def pushed(self):
        pass

    def pushed_initial_index(self):
        pass

    def static_collision_initialized(self):
        pass

    def flashing_collision_initialized(self):
        pass

    def collision_detected(self):
        src_radius = self.specification.penguin.radius
        src_velocity = self.specification.penguin.flash_velocity
        dst_radius = self.specification.penguin.radius
        dst_velocity = self.specification.penguin.flash_velocity

        offsets = collision_offsets_for_circle_bodies(src_radius, src_velocity, dst_radius, dst_velocity)
        compacted_offsets = compact_2d_points(offsets)

        builder = CaseBuilder()

        for x, y in compacted_offsets:
            opponent_x_expr = ExpressionBuilder(Identifier(K_PENGUIN_OTHER_PENGUIN + "." + K_PENGUIN_X))
            opponent_x_expr.wrap_next()

            x_expr = ExpressionBuilder(Identifier(K_PENGUIN_X))
            x_expr.wrap_next()
            x_expr.append_subtract(opponent_x_expr.expression)
            x_expr.wrap_paranthesis()
            x_expr.append_eq(Integer(x))

            opponent_y_expr = ExpressionBuilder(Identifier(K_PENGUIN_OTHER_PENGUIN + "." + K_PENGUIN_Y))
            opponent_y_expr.wrap_next()

            y_expr = ExpressionBuilder(Identifier(K_PENGUIN_Y))
            y_expr.wrap_next()
            y_expr.append_subtract(opponent_y_expr.expression)
            y_expr.wrap_paranthesis()

            if type(y) == range:
                y_expr.append_in(Range.from_range(y))
            else:
                y_expr.append_eq(y)

            x_expr.append_and(y_expr.expression)

            builder.add_case(x_expr.expression, Bool.true())

        builder.add_case(Bool.true(), Bool.false())

        return builder.build()

    def dead_point_reached(self):
        center = (self.specification.island.center_x, self.specification.island.center_y)
        a = self.specification.island.small_radius
        b = self.specification.island.big_radius

        move_dead_points = reachable_points_from_ellipsis(center, a, b, self.specification.penguin.move_velocity)
        flash_dead_points = reachable_points_from_ellipsis(center, a, b, self.specification.penguin.flash_velocity)
        compacted_points = compact_2d_points(list(move_dead_points.union(flash_dead_points)))

        builder = CaseBuilder()

        for x, y in compacted_points:
            x_expr = ExpressionBuilder(K_PENGUIN_X)
            x_expr.wrap_next()
            x_expr.append_eq(Integer(x))

            y_expr = ExpressionBuilder(K_PENGUIN_Y)
            y_expr.wrap_next()

            if type(y) == range:
                y_expr.append_in(Range.from_range(y))
            else:
                y_expr.append_eq(y)

            x_expr.append_and(y_expr.expression)
            builder.add_case(x_expr.expression, Bool.true())

        builder.add_case(Bool.true(), Bool.false())

        return builder.build()
