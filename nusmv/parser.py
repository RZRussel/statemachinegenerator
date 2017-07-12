import yaml
from nusmv.model import *
from nusmv.specification import *
import string


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

    nusmv_modules = parse_modules_from_string(code)
    for nusmv_module in nusmv_modules:
        for i in range(0, len(nusmv_module.code)):
            if nusmv_module.code[i] == '<':
                if origin >= 0:
                    raise ParsingError("Unexpected < symbol while parsing tag")
                origin = i

            if nusmv_module.code[i] == '>':
                if origin == -1:
                    raise ParsingError("Unexpected tag close symbol >")

                if i - origin == 1:
                    raise ParsingError("Empty tag found")

                replacement = Replacement(nusmv_module.name, nusmv_module.code[origin + 1:i],
                                          nusmv_module.origin + origin, i - origin + 1)
                template.add_replacement(replacement)
                origin = -1

    return template


def parse_modules_from_file(filename):
    """
    Creates list of NuSMVModule objects from the content of file
    :param filename: nusmv test cases file's name
    :return: list of NuSMVModule objects
    """
    with open(filename) as file:
        code = file.read()
    return parse_modules_from_string(code)


def parse_modules_from_string(code):
    """
    Parses nusmv code string to separate modules. Algorithm searches modules by
    'MODULE' keyword
    :param code: nusmv code string
    :return: List of NuSMVModule objects
    """

    name_origin = -1
    name_length = 0
    nusmv_modules = []
    module_keyword_length = len(ModuleParserStateMachine.ModuleParserStateExpecting.K_MODULE)

    state_machine = ModuleParserStateMachine()

    for i in range(0, len(code)):
        prev_state = state_machine.state
        state_machine.accept(code[i])

        if type(state_machine.state) == ModuleParserStateMachine.ModuleParserStateNameStart:
            if name_origin >= 0:
                module_name = code[name_origin:name_origin+name_length]
                module_code = code[name_origin-module_keyword_length:i-module_keyword_length+1]
                nusmv_modules.append(NuSMVModule(module_name, module_code, name_origin-module_keyword_length,
                                                 len(module_code)))
            name_origin = i + 1

        if (type(state_machine.state) != ModuleParserStateMachine.ModuleParserStateNameProgress
           and type(prev_state) == ModuleParserStateMachine.ModuleParserStateNameProgress):
            name_length = i - name_origin

    if name_origin >= 0:
        module_name = code[name_origin:name_origin + name_length]
        module_code = code[name_origin - module_keyword_length:len(code)]
        nusmv_modules.append(NuSMVModule(module_name, module_code, name_origin-module_keyword_length,
                                         len(module_code)))

    return nusmv_modules


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


class ModuleParserStateMachine:
    """
    Class is designed to provide state machine interface for parsing nusmv modules.
    Basically the state machine can detect module's beginning and name. Starting from expecting state,
    machine accepts module keyword, name and then switches to the content state to wait
    newline symbol which is always must precede non first module's.
    """

    class ModuleParserStateExpecting:
        K_MODULE = 'MODULE '

        def __init__(self, machine):
            self.machine = machine
            self.progress = 0

        def accept(self, symbol):
            if symbol == self.K_MODULE[self.progress]:
                self.progress = self.progress + 1
                if self.progress == len(self.K_MODULE):
                    self.machine.state = ModuleParserStateMachine.ModuleParserStateNameStart(self.machine)
            elif not (self.progress == 0 and symbol in set(string.whitespace)):
                self.machine.state = ModuleParserStateMachine.ModuleParserStateContent(self.machine)

    class ModuleParserStateNameStart:
        def __init__(self, machine):
            self.machine = machine

        def accept(self, symbol):
            if symbol in set(string.ascii_letters).union(set('_')):
                self.machine.state = ModuleParserStateMachine.ModuleParserStateNameProgress(self.machine)
            else:
                raise ParsingError("Unexpected '" + symbol + "' as first module name's symbol")

    class ModuleParserStateNameProgress:
        def __init__(self, machine):
            self.machine = machine

        def accept(self, symbol):
            if symbol not in set(string.ascii_letters).union(set(string.digits)).union(set('_$-')):
                if symbol == '\n':
                    self.machine.state = ModuleParserStateMachine.ModuleParserStateExpecting(self.machine)
                else:
                    self.machine.state = ModuleParserStateMachine.ModuleParserStateContent(self.machine)

    class ModuleParserStateContent:
        def __init__(self, machine):
            self.machine = machine

        def accept(self, symbol):
            if symbol == '\n':
                self.machine.state = ModuleParserStateMachine.ModuleParserStateExpecting(self.machine)

    def __init__(self):
        self.state = self.ModuleParserStateExpecting(self)

    def accept(self, symbol):
        if type(symbol) != str or len(symbol) != 1:
            raise TypeError("Expected symbol as input")

        self.state.accept(symbol)
