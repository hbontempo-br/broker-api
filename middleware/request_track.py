from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING, NoReturn

from utils.logger import RequestTrack

if TYPE_CHECKING:
    from falcon import Request, Response
    from api.resources.base_resource import BaseResource


class RequestTrackMiddleware:
    def process_request(self, req: Request, res: Response) -> NoReturn:
        new_request_track_id = req.get_header("request-track-id")
        if not new_request_track_id:
            new_request_track_id = str(uuid.uuid4())
            logging.debug(f"New request-track-id generated: {new_request_track_id}")
        RequestTrack.set_request_track_id(new_request_track_id)
        logging.debug("Request Track ID loaded")

    def process_response(
        self, req: Request, res: Response, resource: BaseResource, req_succeeded: bool
    ) -> NoReturn:
        res.set_headers(
            headers={"request-track-id": RequestTrack.get_request_track_id()}
        )
        RequestTrack.clear_request_track_id()
