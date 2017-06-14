import math


def velocity_extrapolation(moving_point, velocity):
    velocities = {}

    for i in range(0, velocity):
        velocities[i] = []

    for i in range(0, 359):
        moving_angle = math.radians(i)
        pushing_vector = -moving_point[0], -moving_point[1]

        if moving_point[0] != 0:
            pushing_angle = math.atan(math.fabs(pushing_vector[1])/math.fabs(pushing_vector[0]))
        else:
            pushing_angle = math.pi/2.0

        if pushing_vector[0] <= 0 and pushing_vector[1] <= 0:
            pushing_angle += math.pi
        elif pushing_vector[0] >= 0 and pushing_vector[1] <= 0:
            pushing_angle = 2.0*math.pi - pushing_angle
        elif pushing_vector[0] <= 0 and pushing_vector[1] >= 0:
            pushing_angle = math.pi - pushing_angle

        result_angle = moving_angle - pushing_angle
        if -math.pi/2.0 <= result_angle <= math.pi/2.0:
            final_velocity = int(round(velocity*math.cos(result_angle)))
            velocities[final_velocity] += [result_angle]

    return velocities


def circle_points(radius):
    if radius <= 0:
        raise Exception("Radius must be positive")

    points = []
    for x in range(0, radius):
        for y in range(0, radius):
            if x*x + y*y <= radius*radius:
                points += [(x, y)]

    return points
