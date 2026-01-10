import unittest

from .network_retrieve import network_retrieve

class CoverageTests(unittest.TestCase):
    def test_network_retrieve(self):
        res = network_retrieve()
        self.assertEqual(res,'<html><body>You are being <a href="https://git.uwaterloo.ca/users/sign_in">redirected</a>.</body></html>')
