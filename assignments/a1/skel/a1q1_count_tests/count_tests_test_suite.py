# from parent directory, run:
#  > python3 -m unittest count_tests.count_tests_test_suite
# or:
#  > python3-coverage run -m unittest count_tests.count_tests_test_suite
#  > python3-coverage run --branch -m unittest count_tests.count_tests_test_suite
#  > python3-coverage report -m
#  > python3-coverage html

import unittest
from . import count_tests

class CoverageTests (unittest.TestCase):
    def test_one(self):
        rv = count_tests.tests_in_file_contents(["TEST_CASE"])
        self.assertEqual(rv, 1)

