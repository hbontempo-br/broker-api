from __future__ import annotations

import logging
from typing import TYPE_CHECKING, NoReturn

from utils.errors import BadRequest, InternalError

if TYPE_CHECKING:
    from falcon import Request, Response
    from api.resources.base_resource import BaseResource


class InputOutputMiddleware:
    def process_resource(
        self, req: Request, res: Response, resource: BaseResource, params: dict
    ) -> NoReturn:
        if not resource:
            return

        try:
            body = req.media
            method = req.method
            path = req.path
            ip_address = req.remote_addr

            logging.info(
                msg=f"INCOMING REQUEST {method} {path} {ip_address} {str(body)}"
            )
        except Exception as ex:
            raise BadRequest(exception=ex).http()

    def process_response(
        self, req: Request, res: Response, resource: BaseResource, req_succeeded: bool
    ) -> NoReturn:

        if not resource:
            return

        try:
            body = res.media
            status = res.status
            method = req.method
            path = req.path
            ip_address = req.remote_addr

            logging.info(
                msg=f"OUTGOING RESPONSE {status} {method} {path} {ip_address} {str(body)}"
            )
        except Exception as ex:
            raise InternalError(exception=ex).http()
