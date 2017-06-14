import math


def moves(radius):
    if radius <= 0:
        raise Exception("Radius must be positive")

    final_points = [(radius, 0)]
    indexes = [0]

    for i in range(1, 90):
        point = (round(radius * math.cos(math.radians(i))), round(radius * math.sin(math.radians(i))))
        if point != final_points[-1]:
            final_points += [point]
            indexes += [i-1]

    return indexes, final_points


def friction_velocity_extrapolation(mass, friction, initial_velocity, delta):
    if mass <= 0:
        raise Exception("Mass must be positive")
    if friction <= 0:
        Exception("Friction must be positive")
    if initial_velocity <= 0:
        Exception("Initial must be positive")
    if delta <= 0:
        Exception("Delta time must be positive")

    velocities = [initial_velocity]
    indexes = [0]
    i = 1

    while velocities[-1] > 0:
        velocity = int(round(initial_velocity * math.exp(-i*delta*friction/mass)))

        if velocity != velocities[-1]:
            velocities += [velocity]
            indexes += [i-1]
        i += 1

    return indexes, velocities
