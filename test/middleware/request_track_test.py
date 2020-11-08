import unittest

import falcon
from middleware.request_track import RequestTrackMiddleware
from utils.logger import RequestTrack


class TestRequestTrackMiddleware(unittest.TestCase):
    def setUp(self):
        self.middleware = RequestTrackMiddleware()
        self.mock_wsgi_env = {
            "wsgi.input": None,
            "wsgi.errors": [],
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/",
            "QUERY_STRING": "",
            "CONTENT_TYPE": "application/json",
        }

    def tearDown(self) -> None:
        RequestTrack.clear_request_track_id()

    def test_process_request_without_headers(self):
        self.middleware.process_request(
            req=falcon.Request(env=self.mock_wsgi_env), res=None
        )
        self.assertIsNotNone(RequestTrack.get_request_track_id())

    def test_process_request_with_headers(self):
        self.mock_wsgi_env["HTTP_REQUEST_TRACK_ID"] = "test_request_track_id"
        self.middleware.process_request(
            req=falcon.Request(env=self.mock_wsgi_env), res=None
        )
        self.assertEqual(RequestTrack.get_request_track_id(), "test_request_track_id")

    def test_process_response(self):
        RequestTrack.set_request_track_id("test_request_track_id")
        self.middleware.process_response(
            req=None, res=falcon.Response(), resource=None, req_succeeded=None
        )
        self.assertIsNone(RequestTrack.get_request_track_id())
