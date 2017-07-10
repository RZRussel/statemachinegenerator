import yaml
from nusmv.model import *
from nusmv.specification import *

class ParsingError(Exception):
    """Exception class to throw if error occures during parsing"""

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description


def parse_template_from_file(filename):
    """
    Creates VerificationTemplate object from the content of file
    :param filename: nusmv verification template file's name
    :return: VerificationTemplate object
    """

    with open(filename) as file:
        code = file.read()
    return parse_template_from_string(code)


def parse_template_from_string(code):
    """
    Parses string and creates VerificationTemplate object. Algorithm searches for tags with
    pattern '<tag>' to create replacement objects for template.
    :param code: nusmv code string
    :return: VerificationTemplate
    """

    origin = -1
    template = VerificationTemplate(code)

    for i in range(0, len(code)):
        if code[i] == '<':
            if origin >= 0:
                raise ParsingError("Unexpected < symbol while parsing tag")
            origin = i

        if code[i] == '>':
            if origin == -1:
                raise ParsingError("Unexpected tag close symbol >")

            if i - origin == 1:
                raise ParsingError("Empty tag found")

            replacement = Replacement(code[origin + 1:i], origin, i - origin + 1)
            template.add_replacement(replacement)
            origin = -1

    return template


def parse_test_cases_from_file(filename):
    """
    Creates list of TestCase objects from the content of file
    :param filename: nusmv test cases file's name
    :return: list of TestCase objects
    """
    with open(filename) as file:
        code = file.read()
    return parse_test_cases_from_string(code)


def parse_test_cases_from_string(code):
    """
    Parses nusmv code string to separate test cases represented as modules. Algorithm searches modules by
    'MODULE' keyword
    :param code: nusmv code string
    :return: list TestCase objects
    """
    new_module_expected = True
    origin = -1
    progress = 0
    pattern = "MODULE "
    test_cases = []

    for i in range(0, len(code)):
        if code[i] == '\n':
            new_module_expected = True
            progress = 0
        elif code[i] in " \t" and new_module_expected and progress == 0:
            continue
        elif new_module_expected and pattern[progress] == code[i]:
            progress = progress + 1
            if progress == len(pattern):
                if origin >= 0:
                    test_code = code[origin:i-progress]
                    test_cases.append(TestCase(test_code.strip(' \n\t\r')))
                origin = i - progress + 1
                new_module_expected = False
        else:
            new_module_expected = False

    if origin >= 0:
        test_code = code[origin:len(code)]
        test_cases.append(TestCase(test_code.strip(' \n\t\r')))

    return test_cases


def parse_specification_from_file(filename):
    """
    Parses yaml file to create specification object
    :param filename: yaml file's name
    :return: Specification object
    """
    with open(filename) as file:
        yaml_string = file.read()
    return parse_specification_from_string(yaml_string)


def parse_specification_from_string(yaml_string):
    """
    Parses yaml game specification. Algorithm uses explicit key references to
    prevent from malicious data injection.
    :param yaml_string: Game specification string in yaml format
    :return: Specification object
    """
    mappings = yaml.load(yaml_string)
    world_mappings = mappings["specification"]["world"]
    island_mappings = mappings["specification"]["island"]
    penguin_mappings = mappings["specification"]["penguin"]
    snowball_mappings = mappings["specification"]["snowball"]

    if "insertions" in mappings["specification"]:
        insertions_mappings = mappings["specification"]["insertions"]
        return Specification(world_mappings, island_mappings, penguin_mappings, snowball_mappings, insertions_mappings)
    else:
        return Specification(world_mappings, island_mappings, penguin_mappings, snowball_mappings)
