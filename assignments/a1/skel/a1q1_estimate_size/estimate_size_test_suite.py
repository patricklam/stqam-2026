# from parent directory, run:
#  > python3 -m unittest estimate_size.estimate_size_test_suite
# or:
#  > python3-coverage run -m unittest estimate_size.estimate_size_test_suite
#  > python3-coverage run --branch -m unittest estimate_size.estimate_size_test_suite
#  > python3-coverage report -m
#  > python3-coverage html

import unittest
from . import estimate_size

class CoverageTests (unittest.TestCase):
    def test_one(self):
        rv = estimate_size.estimate_size(1)
        self.assertEqual(rv, 1)
