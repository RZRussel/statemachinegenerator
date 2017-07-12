from nusmv.model import *
from nusmv.specification import *
from nusmv.generator import *
from copy import *


class Compiler:
    def __init__(self, template, specification, penguin_generator, snowball_generator):
        if type(template) != VerificationTemplate:
            raise TypeError("Expected template of VerificationTemplate class")

        if type(specification) != Specification:
            raise TypeError("Expected specification of Specification class")

        if type(penguin_generator) != PenguinGenerator:
            raise TypeError("Expected penguin_generator of PenguinGenerator class")

        if type(snowball_generator) != SnowballGenerator:
            raise TypeError("Expected snowball_generator of SnowballGenerator class")

        self.template = template
        self.specification = specification
        self.penguin_generator = penguin_generator
        self.snowball_generator = snowball_generator

        self.__process_template()

    def compile(self, test_case=None):
        if test_case is not None:
            main_code = "MODULE Main\n  VAR test: " + test_case.module_name + ";\n"
            return self.model_code + "\n\n" + main_code
        else:
            return self.model_code

    def __process_template(self):
        self.model_code = deepcopy(self.template.code)

        for replacement in reversed(self.template.replacements):
            if replacement.module_name == self.snowball_generator.MODULE_NAME:
                result = getattr(self.snowball_generator, replacement.tag)()
                self.model_code = self.model_code[:replacement.origin] + result \
                                  + self.model_code[replacement.origin + replacement.length:]