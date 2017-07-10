from functools import reduce


def compact_2d_points(points, axis=0):
    """
    Creates list of tuples with first element as corresponding axis value and range of
    consecutive values of the other one. If a range contains only one value than it is replaced with that value.

    For example:
    >>> compact_2d_points([(1, 1), (1, 2), (1, 4), (2, 1), (2, 2)])
    [(1, range(1, 3)), (1, 4), (2, range(1, 3))]
    >>> compact_2d_points([(1, 1), (1, 1)])
    [(1, 1)]
    >>> compact_2d_points([])
    []
    >>> compact_2d_points([(1, 1), (1, 0)])
    [(1, range(0, 2))]

    :param points: List of (x, y) tuples with integer values
    :param axis: 0 or 1 value to pick key axis
    :return: List of tuples with first element of int type and second one range or int.
    """

    cp = []
    origin = 0
    sp = sorted(points)
    for i in range(1, len(sp) + 1):
        if i == len(sp) or sp[origin][axis] != sp[i][axis] or sp[i][1-axis] - sp[origin][1-axis] > 1:
            key = sp[origin][axis]

            if sp[i - 1][1-axis] - sp[origin][1-axis] > 0:
                value = range(sp[origin][1-axis], sp[i - 1][1-axis] + 1)
            else:
                value = sp[origin][1-axis]

            if axis == 0:
                cp.append((key, value))
            else:
                cp.append((value, key))

            origin = i

    return cp


if __name__ == "__main__":
    import doctest
    doctest.testmod()
