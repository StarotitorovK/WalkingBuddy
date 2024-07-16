import queue
import unittest
from PrefUpdater import prepare_pref_data, InputPrefData, PreparedPrefData, MainPrefData, tags_recalc


class TestPrefUpdater(unittest.TestCase):

    def test_prepare_pref_data(self):
        testcase = [InputPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}, rate=1),
                    InputPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}, rate=0.5),
                    InputPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}, rate=-1)]
        self.assertEqual(prepare_pref_data(testcase[0]).tags, {'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0})
        self.assertEqual(prepare_pref_data(testcase[1]).tags, {'бар': 0.5, 'тихий': 0.5, 'исторический': 0.5})
        self.assertEqual(prepare_pref_data(testcase[2]).tags, {'бар': -1.0, 'тихий': -1.0, 'исторический': -1.0})

    def test_tags_recalc_cache_update(self):
        test_queues = [queue.Queue(maxsize=2), queue.Queue(maxsize=2)]
        test_queues[1].put({'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0})
        testcase = [(PreparedPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}),
                     MainPrefData(old_tags={}, cached_tags=test_queues[0], seen=3)),
                    (PreparedPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}),
                     MainPrefData(old_tags={}, cached_tags=test_queues[1], seen=3)),
                    (PreparedPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}),
                     MainPrefData(old_tags={'бар': 1.0, 'тихий': .5, 'исторический': 0}, cached_tags=test_queues[0],
                                  seen=3))
                    ]
        self.assertEqual(tags_recalc(*testcase[0]).cached_tags.qsize(), 1)
        self.assertEqual(tags_recalc(*testcase[1]).cached_tags.qsize(), 2)
        self.assertEqual(tags_recalc(*testcase[2]).old_tags, {'бар': 1.0, 'тихий': .5, 'исторический': 0})

    def test_tags_recalc_weights(self):
        test_queues = [queue.Queue(maxsize=2), queue.Queue(maxsize=2), queue.Queue(maxsize=2)]
        test_queues[0].put({'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0})
        test_queues[1].put({'бар': .5, 'тихий': .5, 'исторический': .5})
        test_queues[2].put({'бар': -1.0, 'тихий': -1.0, 'исторический': -1.0})
        for i in range(3):
            test_queues[i].put({'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0})

        testcase = [(PreparedPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}),
                     MainPrefData(old_tags={'бар': 1.0, 'тихий': .5, 'исторический': 0}, cached_tags=test_queues[0],
                                  seen=3)),
                    (PreparedPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}),
                     MainPrefData(old_tags={'бар': 1.0, 'тихий': .5, 'исторический': 0}, cached_tags=test_queues[1],
                                  seen=3)),
                    (PreparedPrefData(tags={'бар': 1.0, 'тихий': 1.0, 'исторический': 1.0}),
                     MainPrefData(old_tags={'бар': 1.0, 'тихий': .5, 'исторический': 0}, cached_tags=test_queues[2],
                                  seen=3))]
        self.assertEqual(tags_recalc(*testcase[0]).old_tags, {'бар': 1.0, 'тихий': .625, 'исторический': .25})
        self.assertEqual(tags_recalc(*testcase[1]).old_tags, {'бар': .875, 'тихий': 0.5, 'исторический': .125})
        self.assertEqual(tags_recalc(*testcase[2]).old_tags, {'бар': .5, 'тихий': .125, 'исторический': 0})


if __name__ == "__main__":
    unittest.main()
