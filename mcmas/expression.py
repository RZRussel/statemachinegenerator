"""
Classes represents syntax for specific MCMAS expressions
"""

class Bool:
    def __init__(self, value: bool):
        self.value = value

    @staticmethod
    def true():
        return Bool(True)

    @staticmethod
    def false():
        return Bool(False)

    def __str__(self):
        if self.value:
            return "true"
        else:
            return "false"
