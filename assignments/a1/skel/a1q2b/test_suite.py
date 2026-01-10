import unittest

from .count_characters import CharacterCounterClass

class CoverageTests(unittest.TestCase):
    def test_count_characters(self):
        cc = CharacterCounterClass()
        cc.open_file()
        res = cc.count_characters()
        cc.close_file()
        self.assertEqual(res,452)
