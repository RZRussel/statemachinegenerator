

class Replacement:
    """Class is designed to store replacement information of the verification template such as module name, tag
    and range"""

    def __init__(self, agent_name: str, tag: str, origin: int, length: int):
        if len(agent_name) == 0:
            raise ValueError("Agent's name must not be empty")

        if len(tag) == 0:
            raise ValueError("Tag must not be empty")

        self.agent_name = agent_name
        self.tag = tag
        self.origin = origin
        self.length = length

    def __eq__(self, other):
        return self.tag == other.tag and self.origin == other.origin and self.length == other.length


class VerificationTemplate:
    """Class is designed to store replacements for single mcmas verification template"""

    def __init__(self, code: str, replacements=None):
        self.code = code
        self.replacements = replacements or []

    def add_replacement(self, replacement):
        self.replacements.append(replacement)

    def remove_replacement(self, replacement):
        self.replacements.remove(replacement)

    def remove_all_replacements(self):
        self.replacements = []


class MCMASAgent:
    """Class is designed to store mcmas agent's code"""

    def __init__(self, name: str, code: str, origin: int, length: int):
        self.name = name
        self.code = code
        self.origin = origin
        self.length = length
