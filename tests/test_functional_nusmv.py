import unittest
import os
import smv
import shutil

K_SPEC_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], "../resources/test_specification.yaml")
K_TEMPLATE_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], "../resources/template.smv")
K_TEST_CASE_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], "../resources/movement_behavior.smv")
K_TEST_DIRECTORY = os.path.join(os.path.split(os.path.realpath(__file__))[0], "../resources/test")


class TestNuSMVModule(unittest.TestCase):
    def test_with_template_and_specification(self):
        argv = ["-s", K_SPEC_PATH, "-t", K_TEMPLATE_PATH]

        smv.main(argv)

        base_path, filename = os.path.split(K_TEMPLATE_PATH)
        path_parts = filename.rsplit('.', 1)
        result_path = str(path_parts[0]) + smv.K_MODEL_FILE_SUFFIX

        assert os.access(result_path, os.F_OK)

        os.remove(result_path)

    def test_with_template_and_specification_and_test_case_and_directory(self):
        argv = ["-s", K_SPEC_PATH, "-t", K_TEMPLATE_PATH, "-c", K_TEST_CASE_PATH, "-d", K_TEST_DIRECTORY]

        smv.main(argv)

        base_path, filename = os.path.split(K_TEST_CASE_PATH)
        path_parts = filename.rsplit('.', 1)
        result_path = os.path.join(K_TEST_DIRECTORY, str(path_parts[0]) + smv.K_MODEL_FILE_SUFFIX)

        assert os.access(result_path, os.F_OK)

        shutil.rmtree(K_TEST_DIRECTORY)
