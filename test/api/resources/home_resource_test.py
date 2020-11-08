import os
import unittest

import falcon
from api.resources.home_resource import HomeResource


class TestHomeResource(unittest.TestCase):
    def setUp(self):
        self.home = HomeResource()

    def test_on_get(self):
        response = falcon.Response()

        self.home.on_get(req=None, res=response)

        self.assertEqual(response.status, falcon.HTTP_OK)
        expected_body = {"broker-api": "local", "id": str(os.getpid())}
        self.assertDictEqual(response.media, expected_body)
        self.assertDictEqual(response.headers, {})
