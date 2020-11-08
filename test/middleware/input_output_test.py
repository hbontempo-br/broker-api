import unittest

import falcon
from api.resources.base_resource import BaseResource
from middleware.input_output import InputOutputMiddleware


class TestInputOutputMiddleware(unittest.TestCase):
    def setUp(self):
        self.middleware = InputOutputMiddleware()
        self.mock_wsgi_env = {
            "wsgi.input": None,
            "wsgi.errors": [],
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/",
            "QUERY_STRING": "",
            "CONTENT_TYPE": "application/json",
            "REMOTE_ADDR": "0.0.0.0",
        }

    def test_process_resource_without_resource(self):
        with self.assertRaises(AssertionError):
            with self.assertLogs("", level="INFO"):
                self.middleware.process_resource(
                    req=falcon.Request(env=self.mock_wsgi_env),
                    res=None,
                    resource=None,
                    params=None,
                )

    def test_process_resource_with_resource(self):
        with self.assertLogs("", level="INFO") as cm:
            self.middleware.process_resource(
                req=falcon.Request(env=self.mock_wsgi_env),
                res=None,
                resource="A resource",
                params=None,
            )
            self.assertEqual(
                cm.output, ["INFO:root:INCOMING REQUEST GET / 0.0.0.0 None"]
            )

    def test_process_response_without_resource(self):
        with self.assertRaises(AssertionError):
            with self.assertLogs("", level="INFO"):
                self.middleware.process_response(
                    req=falcon.Request(env=self.mock_wsgi_env),
                    res=None,
                    resource=None,
                    req_succeeded=None,
                )

    def test_process_response_with_resource(self):
        response = falcon.Response()
        BaseResource.generate_response(
            res=response, status_code=200, body_dict={"test": "ok"}
        )
        with self.assertLogs("", level="INFO") as cm:
            self.middleware.process_response(
                req=falcon.Request(env=self.mock_wsgi_env),
                res=response,
                resource="A resource",
                req_succeeded=None,
            )
            self.assertEqual(
                cm.output,
                ["INFO:root:OUTGOING RESPONSE 200 OK GET / 0.0.0.0 {'test': 'ok'}"],
            )
