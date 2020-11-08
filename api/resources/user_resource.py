from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from falcon import falcon
from sqlalchemy.orm.exc import NoResultFound
from utils.errors import BadRequest, NotFound, request_error_handler
from utils.schema_validator import get_specification, validate_schema

from ..controllers.user_controller import UserController
from ..DTOs.user_DTO import UserDTO
from .base_resource import BaseResource

# To avoid circular imports because of the type hinting
if TYPE_CHECKING:
    from falcon import Request, Response
    from sqlalchemy.orm import sessionmaker


USER_POST_SCHEMA_DICT = get_specification(schema_name="UserRequest")


class UserResource(BaseResource):
    def __init__(
        self,
        session_factory: sessionmaker,
        user_controller: UserController = UserController(),
    ):
        self.session_factory = session_factory
        self.user_controller = user_controller

    @request_error_handler
    def on_get(self, req: Request, res: Response) -> NoReturn:
        name = req.get_param("name", default=None)
        document = req.get_param("document", default=None)
        email = req.get_param("email", default=None)

        page = req.get_param_as_int("page", min_value=1, default=1)
        page_size = req.get_param_as_int("page_size", min_value=1, default=10)

        # TODO: Add some validation to page and page_size

        db_session = self.session_factory()
        try:
            user_list, total_count = self.user_controller.get_paginated_list(
                session=db_session,
                name=name,
                document=document,
                email=email,
                page_number=page,
                page_size=page_size,
            )
            result_list = [UserDTO(user).to_dict() for user in user_list]
            paginated_response = self.new_paginated_response(
                returned_items=result_list,
                page=page,
                rows_per_page=page_size,
                total_count=total_count,
            )
            self.generate_response(
                res=res,
                status_code=200,
                body_dict=paginated_response,
            )
        except Exception:
            raise
        finally:
            db_session.close()

    @request_error_handler
    @falcon.before(action=validate_schema, schema_dict=USER_POST_SCHEMA_DICT)
    def on_post(self, req: Request, res: Response) -> NoReturn:
        name = req.media.get("name")
        document = req.media.get("document")
        email = req.media.get("email")

        # TODO: Add validation to document and email

        db_session = self.session_factory()
        try:
            user = self.user_controller.create(
                session=db_session, name=name, document=document, email=email
            )

            db_session.commit()

            response_obj = UserDTO(user_model=user)
            self.generate_response(
                res=res, status_code=200, body_dict=response_obj.to_dict()
            )
        except Exception:
            db_session.rollback()
            raise
        finally:
            db_session.close()

    @request_error_handler
    def on_get_with_user_key(
        self, req: Request, res: Response, user_key: str
    ) -> NoReturn:
        db_session = self.session_factory()
        try:
            user = self.user_controller.get_one(session=db_session, user_key=user_key)
            response_obj = UserDTO(user_model=user)
            self.generate_response(
                res=res, status_code=200, body_dict=response_obj.to_dict()
            )
        except NoResultFound:
            raise NotFound().http()
        except Exception:
            raise
        finally:
            db_session.close()

    @request_error_handler
    def on_delete_with_user_key(
        self, req: Request, res: Response, user_key: str
    ) -> NoReturn:
        db_session = self.session_factory()
        try:
            user = self.user_controller.get_one(
                session=db_session, user_key=user_key, lock=True
            )
            user.deleted_at = self.user_controller.db_now()
            self.generate_response(res=res, status_code=204, body_dict=None)
            db_session.commit()
        except NoResultFound:
            db_session.rollback()
            raise BadRequest().http()
        except Exception:
            db_session.rollback()
            raise
        finally:
            db_session.close()
