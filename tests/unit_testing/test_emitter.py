import unittest

from pyramid import testing
from cinchworm import segmenter as seg


class EmitterTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_single_segment(self):
        data = [1, 1, 2, 3, 5]
        segments = seg.Segmenter(data).segments()
        # the header for each binary segment
        # 1. the minimum value for the segment, represented as a 3 byte integer
        min = bytearray(b'\x00\x00\x01')  # 1
        # 2. the length of the segment, represented as a 2 byte integer
        size = bytearray(b'\x00\x05')  # 5
        # 3. the data in the segment, represented as 2 byte integers
        bindata = bytearray(b'\x00\x00\x00\x00\x00\x01\x00\x02\x00\x04')
        expected = min + size + bindata
        self.assertEqual(segments[0].emit(), expected)
