import logging
from functools import wraps
from typing import Callable

import falcon


class BaseError:
    def __init__(
        self,
        title: str,
        description: str,
        http_status: str,
        log_level: int = logging.WARN,
        exception: Exception = None,
    ):
        self.title = title
        self.description = description
        self.exception = exception
        self.log_level = log_level
        self.http_status = http_status

        # TODO: log the correct file where the error happened
        logging.log(
            level=self.log_level, msg=self.__format_msg(), exc_info=self.exception
        )

    def http(self) -> falcon.HTTPError:
        return falcon.HTTPError(self.http_status, self.title, self.description)

    def __format_msg(self) -> str:
        return f"[{self.title}] {self.description}"


class InternalError(BaseError):
    def __init__(
        self,
        title="Internal Error",
        http_status=falcon.HTTP_500,
        description="An internal error has occurred and its being investigated.",
        exception=None,
    ):
        super().__init__(
            title=title,
            description=description,
            http_status=http_status,
            exception=exception,
            log_level=logging.CRITICAL,
        )


class BadRequest(BaseError):
    def __init__(
        self,
        title="Bad Request",
        http_status=falcon.HTTP_400,
        description="The server cannot or will not process the request due to an apparent client error "
        "(e.g., malformed request syntax, size too large, invalid request message framing, or "
        "deceptive request routing)",
        exception=None,
    ):
        super().__init__(
            title=title,
            description=description,
            http_status=http_status,
            exception=exception,
            log_level=logging.INFO,
        )


class NotFound(BaseError):
    def __init__(
        self,
        title="Not Found",
        http_status=falcon.HTTP_404,
        description="The requested resource could not be found but may be available in the future. "
        "Subsequent requests by the client are permissible",
        exception=None,
    ):
        super().__init__(
            title=title,
            description=description,
            http_status=http_status,
            exception=exception,
            log_level=logging.INFO,
        )


class MethodNotAllowed(BaseError):
    def __init__(
        self,
        title="Method Not Allowed",
        http_status=falcon.HTTP_405,
        description="The requested is not supported by the target resource",
        exception=None,
    ):
        super().__init__(
            title=title,
            description=description,
            http_status=http_status,
            exception=exception,
            log_level=logging.INFO,
        )


class Conflict(BaseError):
    def __init__(
        self,
        title="Conflict",
        http_status=falcon.HTTP_409,
        description="Resource already exists",
        exception=None,
    ):
        super().__init__(
            title=title,
            description=description,
            http_status=http_status,
            exception=exception,
            log_level=logging.INFO,
        )


def request_error_handler(function: Callable):
    @wraps(function)
    def decorated(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except falcon.HTTPError as http_error:
            raise http_error
        except Exception as ex:
            raise InternalError(exception=ex).http()

    return decorated
