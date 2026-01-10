import unittest

from . import settings

class CoverageTests(unittest.TestCase):
    def test_provided(self):
        result = settings.VARIANT_TO_RUN('one^|uno||three^^^^|four^^^|^cuatro|')
        self.assertEqual(result, ['one|uno', '', 'three^^', 'four^|cuatro', ''])
    
    def test_statement_coverage(self):
        """Add tests to achieve statement coverage (as many as needed)."""
        # YOUR CODE HERE
        pass

    def test_kill_mutant_1(self):
        """Kill mutant 1"""
        # YOUR CODE HERE
        pass

    def test_kill_mutant_2(self):
        """Kill mutant 2"""
        # YOUR CODE HERE
        pass
