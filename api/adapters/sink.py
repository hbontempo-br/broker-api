from __future__ import annotations

from typing import TYPE_CHECKING

from utils.errors import NotFound

# To avoid circular imports because of the type hinting

if TYPE_CHECKING:
    from falcon import Request, Response


class SinkAdapter:
    def __call__(self, req: Request, resp: Response):
        raise NotFound().http()
