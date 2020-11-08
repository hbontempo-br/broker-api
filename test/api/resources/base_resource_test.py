import unittest

import falcon
from api.resources.base_resource import BaseResource
from utils.errors import MethodNotAllowed


class TestBaseResource(unittest.TestCase):
    def setUp(self) -> None:
        self.base_resource = BaseResource()

    def test_on_get(self):
        with self.assertRaises(
            expected_exception=falcon.http_error.HTTPError
        ) as context:
            self.base_resource.on_get(None, None)
        actual_err = context.exception
        expected_err = MethodNotAllowed().http()
        self.assertEqual(actual_err.code, expected_err.code)
        self.assertEqual(actual_err.status, expected_err.status)
        self.assertEqual(actual_err.title, expected_err.title)
        self.assertEqual(actual_err.description, expected_err.description)

    def test_on_post(self):
        with self.assertRaises(
            expected_exception=falcon.http_error.HTTPError
        ) as context:
            self.base_resource.on_post(None, None)
        actual_err = context.exception
        expected_err = MethodNotAllowed().http()
        self.assertEqual(actual_err.code, expected_err.code)
        self.assertEqual(actual_err.status, expected_err.status)
        self.assertEqual(actual_err.title, expected_err.title)
        self.assertEqual(actual_err.description, expected_err.description)

    def test_on_patch(self):
        with self.assertRaises(
            expected_exception=falcon.http_error.HTTPError
        ) as context:
            self.base_resource.on_patch(None, None)
        actual_err = context.exception
        expected_err = MethodNotAllowed().http()
        self.assertEqual(actual_err.code, expected_err.code)
        self.assertEqual(actual_err.status, expected_err.status)
        self.assertEqual(actual_err.title, expected_err.title)
        self.assertEqual(actual_err.description, expected_err.description)

    def test_on_put(self):
        with self.assertRaises(
            expected_exception=falcon.http_error.HTTPError
        ) as context:
            self.base_resource.on_put(None, None)
        actual_err = context.exception
        expected_err = MethodNotAllowed().http()
        self.assertEqual(actual_err.code, expected_err.code)
        self.assertEqual(actual_err.status, expected_err.status)
        self.assertEqual(actual_err.title, expected_err.title)
        self.assertEqual(actual_err.description, expected_err.description)

    def test_on_delete(self):
        with self.assertRaises(
            expected_exception=falcon.http_error.HTTPError
        ) as context:
            self.base_resource.on_delete(None, None)
        actual_err = context.exception
        expected_err = MethodNotAllowed().http()
        self.assertEqual(actual_err.code, expected_err.code)
        self.assertEqual(actual_err.status, expected_err.status)
        self.assertEqual(actual_err.title, expected_err.title)
        self.assertEqual(actual_err.description, expected_err.description)

    def test_generate_response(self):
        response = falcon.Response()
        status_code = 200
        body_dict = {"body": "ok"}
        headers = {"headers": "ok"}

        self.base_resource.generate_response(
            res=response, status_code=status_code, body_dict=body_dict, headers=headers
        )

        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertEqual(response.media, body_dict)
        self.assertEqual(headers, headers)
