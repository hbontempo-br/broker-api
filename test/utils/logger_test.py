import unittest
from typing import NoReturn

from utils.logger import RequestTrack


class TestRequestTrack(unittest.TestCase):
    def tearDown(self) -> NoReturn:
        RequestTrack.clear_request_track_id()

    def test_set_request_track_id_life_cycle(self):
        expected = "request_track_id"
        RequestTrack.set_request_track_id(expected)
        self.assertEqual(RequestTrack.get_request_track_id(), expected)
        RequestTrack.clear_request_track_id()
        self.assertIsNone(RequestTrack.get_request_track_id())


# class TestLogger(unittest.TestCase):
#
#
