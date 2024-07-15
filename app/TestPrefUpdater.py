import unittest
from PrefUpdater import pref_preparator, InputPrefData, PreparedPrefData

class TestPrefUpdater(unittest.TestCase):

    def test_add(self):
        testcase = [InputPrefData({'бар': 1, 'тихий': 1, 'исторический': 1}, 1),
                    InputPrefData({'бар': 1, 'тихий': 1, 'исторический': 1}, 0.5),
                    InputPrefData({'бар': 1, 'тихий': 1, 'исторический': 1}, -1)]
        self.assertEqual(pref_preparator(testcase[0]).tags, {'бар': 1, 'тихий': 1, 'исторический': 1})
        self.assertEqual(pref_preparator(testcase[1]).tags, {'бар': 0.5, 'тихий': 0.5, 'исторический': 0.5})
        self.assertEqual(pref_preparator(testcase[2]).tags, {'бар': -1, 'тихий': -1, 'исторический': -1})