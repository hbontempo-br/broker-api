import unittest

import falcon
from api.adapters.sink import SinkAdapter
from utils.errors import NotFound


class TestSinkAdapter(unittest.TestCase):
    def test_sink(self):
        with self.assertRaises(
            expected_exception=falcon.http_error.HTTPError
        ) as context:
            SinkAdapter().__call__(None, None)
        actual_err = context.exception
        expected_err = NotFound().http()
        self.assertEqual(actual_err.code, expected_err.code)
        self.assertEqual(actual_err.status, expected_err.status)
        self.assertEqual(actual_err.title, expected_err.title)
        self.assertEqual(actual_err.description, expected_err.description)
