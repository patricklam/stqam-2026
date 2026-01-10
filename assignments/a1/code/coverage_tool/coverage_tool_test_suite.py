# from parent directory, run:
#  > python3 -m unittest coverage_tool.coverage_tool_test_suite

import unittest
from coverage_tool.coverage import *
from coverage_tool.cgi_decode import *

class CoverageTests (unittest.TestCase):
    def test_one(self):
        with Coverage([cd]) as cov:
            cd("a+b")
        self.assertEqual (cov.coverage_stats(), (15, 22, 20, 31))
