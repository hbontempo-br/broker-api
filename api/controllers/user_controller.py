from typing import List, Tuple, Union

from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from ..models import UserModel

# from utils.operations import BasicOperation
from .base_controller import BaseController


class UserController(BaseController):
    def __init__(self):
        BaseController.__init__(self, model=UserModel)

    def create(
        self, session: Session, name: str, document: str, email: str
    ) -> UserModel:
        user = UserModel()
        user.user_key = self.new_key()
        user.name = name
        user.document = document
        user.email = email
        user.balance = 0
        user.created_at = self.db_now()

        self.add(session=session, data=[user])

        return user

    def __filter_by_user_key(
        self, query: Query, user_key: Union[str, List[str]]
    ) -> Query:
        return self._filter(query=query, column=self.model.user_key, value=user_key)

    def __filter_by_name(self, query: Query, name: Union[str, List[str]]) -> Query:
        return self._filter_like(query=query, column=self.model.name, value=name)

    def __filter_by_document(
        self, query: Query, document: Union[str, List[str]]
    ) -> Query:
        return self._filter_like(
            query=query, column=self.model.document, value=document
        )

    def __filter_by_email(self, query: Query, email: Union[str, List[str]]) -> Query:
        return self._filter_like(query=query, column=self.model.email, value=email)

    def __only_active(self, query: Query, only_active: bool = True) -> Query:
        if only_active:
            query = self._filter_is_null(query=query, column=self.model.deleted_at)
        return query

    def __apply_all_filters(
        self,
        query: Query,
        user_key: Union[str, List[str]] = None,
        name: Union[str, List[str]] = None,
        document: Union[str, List[str]] = None,
        email: Union[str, List[str]] = None,
        only_active: bool = True,
        lock: bool = False,
    ) -> Query:
        if user_key:
            query = self.__filter_by_user_key(query=query, user_key=user_key)
        if name:
            query = self.__filter_by_name(query=query, name=name)
        if document:
            query = self.__filter_by_document(query=query, document=document)
        if email:
            query = self.__filter_by_email(query=query, email=email)
        if lock:
            query = self.lock(query=query)
        query = self.__only_active(query=query, only_active=only_active)
        return query

    def get_first(
        self,
        session=Session,
        user_key: Union[str, List[str]] = None,
        name: Union[str, List[str]] = None,
        document: Union[str, List[str]] = None,
        email: Union[str, List[str]] = None,
        only_active: bool = True,
        lock: bool = False,
        **kwargs,
    ) -> UserModel:
        query = self.new_query(session=session)
        query = self.__apply_all_filters(
            query=query,
            user_key=user_key,
            name=name,
            document=document,
            email=email,
            only_active=only_active,
            lock=lock,
        )
        result = super().get_first(query=query)

        return result

    def get_one(
        self,
        session: Session,
        user_key: Union[str, List[str]] = None,
        name: Union[str, List[str]] = None,
        document: Union[str, List[str]] = None,
        email: Union[str, List[str]] = None,
        only_active: bool = True,
        lock: bool = False,
        **kwargs,
    ) -> UserModel:
        query = self.new_query(session=session)
        query = self.__apply_all_filters(
            query=query,
            user_key=user_key,
            name=name,
            document=document,
            email=email,
            only_active=only_active,
            lock=lock,
        )
        result = super().get_one(query=query)

        return result

    def get_one_id(
        self,
        session: Session,
        user_key: Union[str, List[str]] = None,
        name: Union[str, List[str]] = None,
        document: Union[str, List[str]] = None,
        email: Union[str, List[str]] = None,
        only_active: bool = True,
        lock: bool = False,
        **kwargs,
    ) -> int:
        return self.get_one(
            session=session,
            user_key=user_key,
            name=name,
            document=document,
            email=email,
            only_active=only_active,
            lock=lock,
        ).id

    def get_list(
        self,
        session: Session,
        user_key: Union[str, List[str]] = None,
        name: Union[str, List[str]] = None,
        document: Union[str, List[str]] = None,
        email: Union[str, List[str]] = None,
        only_active: bool = True,
        lock: bool = False,
        **kwargs,
    ) -> List[UserModel]:
        query = self.new_query(session=session)
        query = self.__apply_all_filters(
            query=query,
            user_key=user_key,
            name=name,
            document=document,
            email=email,
            only_active=only_active,
            lock=lock,
        )
        result = super().get_all(query=query)

        return result

    def get_paginated_list(
        self,
        session: Session,
        user_key: Union[str, List[str]] = None,
        name: Union[str, List[str]] = None,
        document: Union[str, List[str]] = None,
        email: Union[str, List[str]] = None,
        only_active: bool = True,
        lock: bool = False,
        page_number: int = 1,
        page_size: int = None,
        **kwargs,
    ) -> Tuple[List[UserModel], int]:
        query = self.new_query(session=session)
        query = self.__apply_all_filters(
            query=query,
            user_key=user_key,
            name=name,
            document=document,
            email=email,
            only_active=only_active,
            lock=lock,
        )
        result = super().get_paginated_list(
            query=query, page_number=page_number, page_size=page_size
        )

        return result
