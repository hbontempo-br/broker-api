import unittest
from logging import CRITICAL
from uuid import uuid4

import falcon
from utils.errors import (
    BadRequest,
    BaseError,
    Conflict,
    InternalError,
    MethodNotAllowed,
    NotFound,
    request_error_handler,
)


class TestBaseError(unittest.TestCase):
    def setUp(self):
        self.title = "Title"
        self.description = "Description"
        self.http_status = falcon.HTTP_799
        self.log_level = CRITICAL
        self.exception = AttributeError
        self.error_type = BaseError

    def test_error_logging(self):
        with self.assertLogs(level=self.log_level) as cm:
            self.error_type(
                title=self.title,
                description=self.description,
                http_status=self.http_status,
                log_level=self.log_level,
                exception=self.exception(),
            )
            expected_log = ["CRITICAL:root:[Title] Description\nAttributeError"]
            self.assertEqual(cm.output, expected_log)

    def test_http(self):
        base_error = self.error_type(
            title=self.title,
            description=self.description,
            http_status=self.http_status,
            log_level=self.log_level,
            exception=self.exception(),
        )
        error = base_error.http()
        self.assertEqual(error.status, self.http_status)
        self.assertEqual(error.description, self.description)
        self.assertEqual(error.title, self.title)
        self.assertIsInstance(error, falcon.HTTPError)


class TestInternalError(unittest.TestCase):
    def setUp(self):
        self.title = "Title"
        self.description = "Description"
        self.error_type = InternalError
        self.expected_error = falcon.HTTP_INTERNAL_SERVER_ERROR

    def test_http(self):
        internal_error = self.error_type(title=self.title, description=self.description)
        error = internal_error.http()
        self.assertEqual(error.status, self.expected_error)
        self.assertEqual(error.description, self.description)
        self.assertEqual(error.title, self.title)
        self.assertIsInstance(error, falcon.HTTPError)


class TestBadRequest(unittest.TestCase):
    def setUp(self):
        self.title = "Title"
        self.description = "Description"
        self.error_type = BadRequest
        self.expected_error = falcon.HTTP_BAD_REQUEST

    def test_http(self):
        bad_request_error = self.error_type(
            title=self.title, description=self.description
        )
        error = bad_request_error.http()
        self.assertEqual(error.status, self.expected_error)
        self.assertEqual(error.description, self.description)
        self.assertEqual(error.title, self.title)
        self.assertIsInstance(error, falcon.HTTPError)


class TestNotFound(unittest.TestCase):
    def setUp(self):
        self.title = "Title"
        self.description = "Description"
        self.error_type = NotFound
        self.expected_error = falcon.HTTP_NOT_FOUND

    def test_http(self):
        bad_request_error = self.error_type(
            title=self.title, description=self.description
        )
        error = bad_request_error.http()
        self.assertEqual(error.status, self.expected_error)
        self.assertEqual(error.description, self.description)
        self.assertEqual(error.title, self.title)
        self.assertIsInstance(error, falcon.HTTPError)


class TestMethodNotAllowed(unittest.TestCase):
    def setUp(self):
        self.title = "Title"
        self.description = "Description"
        self.error_type = MethodNotAllowed
        self.expected_error = falcon.HTTP_METHOD_NOT_ALLOWED

    def test_http(self):
        bad_request_error = self.error_type(
            title=self.title, description=self.description
        )
        error = bad_request_error.http()
        self.assertEqual(error.status, self.expected_error)
        self.assertEqual(error.description, self.description)
        self.assertEqual(error.title, self.title)
        self.assertIsInstance(error, falcon.HTTPError)


class TestConflict(unittest.TestCase):
    def setUp(self):
        self.title = "Title"
        self.description = "Description"
        self.error_type = Conflict
        self.expected_error = falcon.HTTP_CONFLICT

    def test_http(self):
        bad_request_error = self.error_type(
            title=self.title, description=self.description
        )
        error = bad_request_error.http()
        self.assertEqual(error.status, self.expected_error)
        self.assertEqual(error.description, self.description)
        self.assertEqual(error.title, self.title)
        self.assertIsInstance(error, falcon.HTTPError)


def ok_function(response):
    return response


def error_function():
    raise Exception()


class TestRequestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.request_error_handler = request_error_handler
        self.ok_function = ok_function
        self.ok_response = str(uuid4())
        self.error_function = error_function
        self.expected_error_type = InternalError().http()

    def test_ok_function(self):
        resp = self.request_error_handler(function=self.ok_function)(self.ok_response)
        self.assertEqual(resp, self.ok_response)

    def test_error_function(self):
        with self.assertRaises(expected_exception=falcon.http_error.HTTPError):
            self.request_error_handler(function=self.error_function)()
