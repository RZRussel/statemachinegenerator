
class Replacement:
    """Class is designed to store replacement information of the verification template such as tag
    and range"""

    def __init__(self, tag, origin, length):
        if type(tag) != str:
            raise TypeError("Expected string type for tag")

        if len(tag) == 0:
            raise Exception("Tap must not be empty")

        if type(origin) != int:
            raise TypeError("Expected int type for origin")

        if type(length) != int:
            raise TypeError("Expected int type for length")

        self.tag = tag
        self.origin = origin
        self.length = length

    def __eq__(self, other):
        return self.tag == other.tag and self.origin == other.origin and self.length == other.length


class VerificationTemplate:
    """Class is designed to store replacements for single nusmv verification template"""

    def __init__(self, code, replacements=None):
        if type(code) != str:
            raise TypeError("Expected string type for code")

        self.code = code
        self.replacements = replacements or []

    def add_replacement(self, replacement):
        self.replacements.append(replacement)

    def remove_replacement(self, replacement):
        self.replacements.remove(replacement)

    def remove_all_replacements(self):
        self.replacements = []


class TestCase:
    """Class is designed to store nusmv test case code represented as a module"""

    def __init__(self, code):
        self.code = code
