import math


def moves(velocity):
    if velocity <= 0:
        raise Exception("Velocity must be positive")

    points = []

    for i in range(0, 360):
        point = (round(velocity * math.cos(math.radians(i))), round(velocity * math.sin(math.radians(i))))
        points += [point]

    return points


def fricvelext(mass, friction, initvel, delta):
    if mass <= 0:
        raise Exception("Mass must be positive")
    if friction <= 0:
        Exception("Friction must be positive")
    if initvel <= 0:
        Exception("Initial must be positive")
    if delta <= 0:
        Exception("Delta time must be positive")

    velocities = [initvel]
    indexes = [0]
    i = 1

    while velocities[-1] > 0:
        velocity = int(round(initvel * math.exp(-i*delta*friction/mass)))

        if velocity != velocities[-1]:
            velocities += [velocity]
            indexes += [i-1]
        i += 1

    return indexes, velocities
