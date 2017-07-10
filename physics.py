from math import *


def radial_moves(velocity):
    """
    Algorithm takes points which lies on the circle with given radius and step 1 degree.
    Than rounds their coordinates.
    will be thrown.
    :param velocity: target's movement velocity. Must be none negative otherwise type error will be thrown.
    :return: List of 360 (x, y) tuples
    """

    if velocity < 0:
        raise TypeError("Velocity must be none negative")

    positions = []
    for i in range(0, 360):
        x = round(velocity * cos(radians(i)))
        y = round(velocity * sin(radians(i)))
        positions.append((x, y))

    return positions


def rotate_position(position):
    """
    Algorithm takes position and generates all it's rotations around (0, 0)
    with 1 degree step. Final coordinates are rounded.
    :param position: (x, y) tuple
    :return: List of 360 (x, y) tuples
    """

    if type(position) != tuple or len(position) != 2:
        TypeError("Position must be valid 2d tuple")

    positions = []
    for i in range(0, 360):
        x = round(position[0]*cos(radians(i)) - position[1]*sin(radians(i)))
        y = round(position[0]*sin(radians(i)) + position[1]*cos(radians(i)))
        positions.append((x, y))

    return positions
