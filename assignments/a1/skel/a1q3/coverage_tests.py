import unittest

from . import settings

class CoverageTests(unittest.TestCase):
    # the first two tests achieve statement coverage
    def test_provided_one(self):
        result = settings.VARIANT_TO_RUN('aaabb')
        self.assertEqual(result, 'a3b2')

    def test_provided_two(self):
        result = settings.VARIANT_TO_RUN('abb')
        self.assertEqual(result, 'a1b2')

    # this test passes the original but fails with mutant 1
    def test_kill_mutant_1(self):
        """Kill mutant 1"""
        # YOUR CODE HERE
        pass

    # this test passes the original but fails with mutant 2
    def test_kill_mutant_2(self):
        """Kill mutant 2"""
        # YOUR CODE HERE
        pass

    # this test fails the original but passes with a fixed version
    def test_bugfix(self):
        # YOUR CODE HERE
        pass
