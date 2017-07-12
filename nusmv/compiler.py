from nusmv.model import *
from nusmv.specification import *
from copy import *


class Compiler:
    """
    Class is designed to generate test case from the specification, template and test case module.
    First of all template's tagged sets are calculated and are inserted. Than test case is inserted if
    and provided in compile method parameter. After that corresponding test case object is created in the main module.
    """
    def __init__(self, template, specification, penguin_generator, snowball_generator):
        if type(template) != VerificationTemplate:
            raise TypeError("Expected template of VerificationTemplate class")

        if type(specification) != Specification:
            raise TypeError("Expected specification of Specification class")

        self.template = template
        self.specification = specification
        self.penguin_generator = penguin_generator
        self.snowball_generator = snowball_generator

        self.__process_template()

    def compile(self, test_case=None):
        if test_case is not None:
            main_code = "MODULE Main\n  VAR\n    test: " + test_case.name + ";\n"
            return self.model_code + "\n" + test_case.code + "\n" + main_code
        else:
            return self.model_code

    def __process_template(self):
        self.model_code = deepcopy(self.template.code)

        for replacement in reversed(self.template.replacements):
            insertion_key = Specification.insertion_key(replacement.module_name, replacement.tag)

            result = None

            if insertion_key in self.specification.insertions:
                result = self.specification.insertions[insertion_key]
            else:
                if replacement.module_name == self.snowball_generator.MODULE_NAME:
                    generator = self.snowball_generator
                else:
                    generator = self.penguin_generator

                if hasattr(generator, replacement.tag):
                    result = getattr(generator, replacement.tag)()

            if result is not None:
                self.model_code = self.model_code[:replacement.origin] + result \
                                  + self.model_code[replacement.origin + replacement.length:]
