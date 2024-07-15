import unittest
from PrefUpdater import prepare_pref_data, InputPrefData, PreparedPrefData


class TestPrefUpdater(unittest.TestCase):

    def test_add(self):
        testcase = [InputPrefData(15, {'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}, 1),
                    InputPrefData(15, {'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}, 0.5),
                    InputPrefData(15, {'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}, -1)]
        self.assertEqual(prepare_pref_data(testcase[0]).tags, {'бар': 1, 'тихий': 1, 'исторический': 1})
        self.assertEqual(prepare_pref_data(testcase[1]).tags, {'бар': 0.5, 'тихий': 0.5, 'исторический': 0.5})
        self.assertEqual(prepare_pref_data(testcase[2]).tags, {'бар': -1, 'тихий': -1, 'исторический': -1})
