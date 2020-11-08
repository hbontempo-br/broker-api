from __future__ import annotations

import os
from typing import TYPE_CHECKING, NoReturn

from constants import COMMIT, SERVICE_NAME
from utils.errors import request_error_handler

from .base_resource import BaseResource

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from falcon import Request, Response


class HomeResource(BaseResource):
    @request_error_handler
    def on_get(self, req: Request, res: Response) -> NoReturn:
        self.generate_response(
            res=res,
            status_code=200,
            body_dict={SERVICE_NAME: COMMIT, "id": str(os.getpid())},
        )
