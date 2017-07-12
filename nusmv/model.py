
class Replacement:
    """Class is designed to store replacement information of the verification template such as module name, tag
    and range"""

    def __init__(self, module_name, tag, origin, length):
        if type(module_name) != str:
            raise TypeError("Expected string type for module_name")

        if type(tag) != str:
            raise TypeError("Expected string type for tag")

        if len(tag) == 0:
            raise Exception("Tap must not be empty")

        if type(origin) != int:
            raise TypeError("Expected int type for origin")

        if type(length) != int:
            raise TypeError("Expected int type for length")

        self.module_name = module_name
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


class NuSMVModule:
    """Class is designed to store nusmv module code"""

    def __init__(self, name, code, origin, length):
        self.name = name
        self.code = code
        self.origin = origin
        self.length = length
