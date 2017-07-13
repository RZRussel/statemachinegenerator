import sys
import getopt
import os
from nusmv.compiler import *
from nusmv.generator import *
from nusmv.parser import *

K_MODEL_FILE_SUFFIX = "_model.smv"


def main(argv):
    """
    Parses command line arguments and executes the process of compiling the template into nusmv executable model.

    Usage: python smv.py -s <specification> -t <template> [-c <list of test cases>] [-d <destination directory>] [-h]

    :param argv: Command line argument list
    :return: No return value
    """

    try:
        opts, args = getopt.getopt(argv, "hs:t:c:d:")
    except getopt.GetoptError:
        print(usage_string())
        sys.exit(2)

    specification_path = None
    template_path = None
    test_case_path = None
    directory = None

    for opt, arg in opts:
        if opt == "-h":
            print(usage_string())
            sys.exit(1)
        elif opt == "-s":
            specification_path = arg
        elif opt == "-t":
            template_path = arg
        elif opt == "-c":
            test_case_path = arg
        elif opt == "-d":
            directory = arg

    if specification_path is None or template_path is None:
        print(usage_string())
        sys.exit(1)

    if not os.path.isabs(specification_path):
        specification_path = os.path.join(os.getcwd(), specification_path)

    if not os.access(specification_path, os.F_OK):
        print("Can't find specification file " + specification_path)
        sys.exit(1)

    if not os.path.isabs(template_path):
        template_path = os.path.join(os.getcwd(), template_path)

    if not os.access(template_path, os.F_OK):
        print("Can't find template file " + template_path)
        sys.exit(1)

    if test_case_path is not None and not os.path.isabs(test_case_path):
        test_case_path = os.path.join(os.getcwd(), test_case_path)

    if test_case_path is not None and not os.access(test_case_path, os.F_OK):
        print("Can't find test case file " + test_case_path)
        sys.exit(1)

    if directory is None:
        directory = os.getcwd()
    elif not os.path.isabs(directory):
        directory = os.path.join(os.getcwd(), directory)

    if not os.access(directory, os.F_OK):
        os.mkdir(directory)

    execute(specification_path, template_path, test_case_path, directory)


def execute(specification_path, template_path, test_case_path, directory):
    specification = parse_specification_from_file(specification_path)
    template = parse_template_from_file(template_path)

    compiler = Compiler(template, specification, PenguinGenerator(specification), SnowballGenerator(specification))

    if test_case_path is not None:
        test_cases = parse_modules_from_file(test_case_path)

        for test_case in test_cases:
            compiled_test_case = compiler.compile(test_case)

            base_path, filename = os.path.split(test_case_path)
            name_parts = filename.rsplit('.', 1)
            result_path = os.path.join(directory, str(name_parts[0]) + K_MODEL_FILE_SUFFIX)

            with open(result_path, "w") as fd:
                fd.write(compiled_test_case)
    else:
        compiled_template = compiler.compile()

        base_path, filename = os.path.split(template_path)
        path_parts = filename.rsplit('.', 1)
        result_path = os.path.join(directory, str(path_parts[0]) + K_MODEL_FILE_SUFFIX)

        with open(result_path, "w") as fd:
            fd.write(compiled_template)


def usage_string():
    """
    Returns details about script usage.
    :return: String value.
    """

    usage = """Usage:\npython smv.py -s <specification> -t <template> [-c <test case>]\
 [-d <destination directory>] [-h]"""
    usage = usage + "\n\n" + "-h\n Optional flag that prints usage of the script."
    usage = usage + "\n\n" + "-s\n Mandatory flag (if no -h flag) to provide path to the yaml specification file."
    usage = usage + "\n\n" + """-t\n Mandatory flag (if no -h flag) to provide path to the nusmv template file.\
 If -c option is not provided than the result file will be named the same as template but with '_model' suffix."""
    usage = usage + "\n\n" + """-c\n Optional flag (if no -h flag) to provide path to the nusmv test case file.\
 Test case model's file is created with test case module's name suffixed '_model' as filename."""
    usage = usage + "\n\n" + """-d\n Optional flag (if no -h flag) to provide path to directory where to save the results.\
 If flag is not provided than result will be save in the current directory."""

    return usage

if __name__ == "__main__":
    main(sys.argv[1:])
