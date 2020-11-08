from __future__ import annotations

from typing import TYPE_CHECKING, Dict, NoReturn

from falcon import get_http_status
from utils.errors import MethodNotAllowed, request_error_handler

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from falcon import Request, Response


class BaseResource:
    @request_error_handler
    def on_get(self, req: Request, res: Response) -> NoReturn:
        raise MethodNotAllowed().http()

    @request_error_handler
    def on_post(self, req: Request, res: Response) -> NoReturn:
        raise MethodNotAllowed().http()

    @request_error_handler
    def on_patch(self, req: Request, res: Response) -> NoReturn:
        raise MethodNotAllowed().http()

    @request_error_handler
    def on_put(self, req: Request, res: Response) -> NoReturn:
        raise MethodNotAllowed().http()

    @request_error_handler
    def on_delete(self, req: Request, res: Response) -> NoReturn:
        raise MethodNotAllowed().http()

    @staticmethod
    def generate_response(
        res: Response, status_code: int, body_dict: dict, headers: Dict = {}
    ) -> NoReturn:
        res.status = get_http_status(status_code=status_code)
        res.media = body_dict
        res.set_headers(headers=headers)
