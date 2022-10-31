import unittest

from pyramid import testing
from cinchworm import segmenter as seg


class SegmenterTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_single_segment(self):
        data = [1, 1, 2, 3, 5]

        s = seg.Segmenter(data)
        self.assertEqual(s.segments()[0].data, data)
        self.assertEqual(len(s.segments()), 1)

    def test_rising_segments(self):
        data = [1, 1, 2, 3, 5, 100000, 100005, 200000, 260000]
        s = seg.Segmenter(data)
        result = s.segments()
        self.assertEqual(len(result), 3)

        # verify first segment
        self.assertEqual(result[0].max, 5)
        self.assertEqual(result[0].min, 1)
        self.assertEqual(result[0].data, [1, 1, 2, 3, 5])
        self.assertEqual(result[0].offset, 0)

        # verify 2nd segment
        self.assertEqual(result[1].max, 100005)
        self.assertEqual(result[1].min, 100000)
        self.assertEqual(result[1].data, [100000, 100005])
        self.assertEqual(result[1].offset, 5)

        # verify 3rd segment
        self.assertEqual(result[2].max, 260000)
        self.assertEqual(result[2].min, 200000)
        self.assertEqual(result[2].data, [200000, 260000])
        self.assertEqual(result[2].offset, 7)

    def test_falling_segments(self):
        data = [100000, 30000, -50000, -60000, -200000, -260000]
        s = seg.Segmenter(data)
        result = s.segments()
        self.assertEqual(len(result), 4)

        # verify first segment
        self.assertEqual(result[0].max, 100000)
        self.assertEqual(result[0].min, 100000)
        self.assertEqual(result[0].data, [100000])
        self.assertEqual(result[0].offset, 0)

        # verify 2nd segment
        self.assertEqual(result[1].max, 30000)
        self.assertEqual(result[1].min, 30000)
        self.assertEqual(result[1].data, [30000])
        self.assertEqual(result[1].offset, 1)

        # verify 3rd segment
        self.assertEqual(result[2].max, -50000)
        self.assertEqual(result[2].min, -60000)
        self.assertEqual(result[2].data, [-50000, -60000])
        self.assertEqual(result[2].offset, 2)

        # verify 4th segment
        self.assertEqual(result[3].max, -200000)
        self.assertEqual(result[3].min, -260000)
        self.assertEqual(result[3].data, [-200000, -260000])
        self.assertEqual(result[3].offset, 4)

    def test_mixed_segments(self):
        data = [1000, 500, -5000, -6000, -64535, -64536,
                0, 1000, 66535, 66536, 67000, 1000000, 80000]
        s = seg.Segmenter(data)
        result = s.segments()
        self.assertEqual(len(result), 6)

        # verify data
        self.assertEqual([s.data for s in result], [[1000, 500, -5000, -6000, -64535],
                         [-64536, 0], [1000, 66535], [66536, 67000], [1000000], [80000]])
