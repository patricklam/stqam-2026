# from parent directory, run:
#  > python3 -m unittest L03.test_suite
# or:
#  > python3-coverage run -m unittest L03.test_suite
#  > python3-coverage run --branch -m unittest L03.test_suite
#  > python3-coverage report -m
#  > python3-coverage html

import unittest

from .foo import Foo

class CoverageTests(unittest.TestCase):
    def test_one(self):
        f = Foo()
        f.m(1, 2)

    def test_two(self):
        f = Foo()
        f.m(1, -2)

    def test_three(self):
        f = Foo()
        f.m(-1, 2)
