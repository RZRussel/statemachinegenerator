"""
Classes represents syntax for specific nusmv expressions
"""


class Range:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @staticmethod
    def from_range(init_range):
        if type(init_range) != range:
            raise TypeError("Range type expected as parameter")

        range_list = list(init_range)
        return Range(range_list[0], range_list[-1])

    def __str__(self):
        return str(self.left) + ".." + str(self.right)


class Bool:
    def __init__(self, value):
        if type(value) != bool:
            raise TypeError("Bool expression expected")

        self.value = value

    @staticmethod
    def true():
        return Bool(True)

    @staticmethod
    def false():
        return Bool(False)

    def __str__(self):
        if self.value:
            return "TRUE"
        else:
            return "FALSE"
