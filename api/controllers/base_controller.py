from typing import Any, List, Tuple, Union
from unicodedata import normalize
from uuid import uuid4

from sqlalchemy import Column, asc, desc, distinct, func, or_
from sqlalchemy.orm import Session, lazyload
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import make_transient
from sqlalchemy.sql.functions import now

# from utils.operations import BasicOperation
from ..models.base_model import BaseModel


class BaseController:
    def __init__(self, model: BaseModel):
        self.model = model

    def add(self, session: Session, data: Union[BaseModel, List[BaseModel]]) -> None:
        if not isinstance(data, list):
            data = [data]
        session.add_all(data)

    def delete(self, session: Session, data: BaseModel) -> None:
        session.delete(data)

    def new_query(self, session: Session) -> Query:
        return session.query(self.model)

    @staticmethod
    def lock(query: Query) -> Query:
        return query.with_for_update()

    @staticmethod
    def get_first(query: Query) -> BaseModel:
        return query.first()

    @staticmethod
    def get_one(query: Query) -> BaseModel:
        return query.one()

    @staticmethod
    def get_all(query: Query) -> List[BaseModel]:
        return query.all()

    @staticmethod
    def get_paginated_list(
        query: Query, page_number: int, page_size: int
    ) -> Tuple[List[BaseModel], int]:
        total_count = BaseController.get_count(query)
        result_list = query.limit(page_size).offset((page_number - 1) * page_size).all()
        return result_list, total_count

    @staticmethod
    def _filter(query: Query, column: Column, value: Any) -> Query:
        if not isinstance(value, list):
            value = [value]
        new_query = query.filter(column.in_(value))
        return new_query

    @staticmethod
    def _filter_like(query: Query, column: Column, value: Any) -> Query:
        if not isinstance(value, list):
            value = [value]
        new_query = query
        for single_value in value:
            new_query = new_query.filter(column.ilike(f"%{single_value}%"))
        return new_query

    @staticmethod
    def _filter_compare(
        query: Query,
        column: Column,
        value: Any,
        type: ["greater", "lesser"],  # noqa: F821
        inclusive: bool = True,
    ) -> Query:

        if type == "greater":
            if inclusive:
                new_query = query.filter(column >= value)
            else:
                new_query = query.filter(column > value)
        elif type == "lesser":
            if inclusive:
                new_query = query.filter(column <= value)
            else:
                new_query = query.filter(column < value)
        else:
            raise AttributeError

        return new_query

    @staticmethod
    def _filter_is_null(query: Query, column: Column):
        return query.filter(column.is_(None))

    @staticmethod
    def _filter_or(
        query: Query, condition_tuple_list: List[Tuple[str, Column, Any]]
    ) -> Query:
        def build_condition(filter_type: str, column: Column, value):
            if filter_type == "like":
                if not isinstance(value, list):
                    value = [value]
                response = [column.like(f"%{single_value}%") for single_value in value]
            else:
                if not isinstance(value, list):
                    value = [value]
                response = [column.in_(value)]
            return response

        condition_list = []
        for condition_tuple in condition_tuple_list:
            condition_list.extend(
                build_condition(
                    filter_type=condition_tuple[0],
                    column=condition_tuple[1],
                    value=condition_tuple[2],
                )
            )

        new_query = query.filter(or_(*condition_list))

        return new_query

    @staticmethod
    def __asc(query: Query, column: Column) -> Query:
        new_query = query.order_by(asc(column))
        return new_query

    @staticmethod
    def __desc(query: Query, column: Column) -> Query:
        new_query = query.order_by(desc(column))
        return new_query

    @staticmethod
    def _order_by(query: Query, column: Column, order: str) -> Query:
        method = {"asc": BaseController.__asc, "desc": BaseController.__desc}
        return method[order](query, column)

    @staticmethod
    def make_copy(model: BaseModel) -> None:
        make_transient(model)
        model.id = None
        model.created_at = None

    @staticmethod
    def new_key() -> str:
        return str(uuid4())

    @staticmethod
    def clean_string(txt) -> str:
        return normalize("NFKD", txt).encode("ASCII", "ignore").decode("ASCII")

    @staticmethod
    def db_now():
        return now()

    @staticmethod
    def get_count(query: Query) -> int:

        # Reference: https://gist.github.com/hest/8798884#gistcomment-2301279

        disable_group_by = False
        if len(query._entities) > 1:
            raise Exception(f"only one entity is supported for get_count, got: {query}")
        entity = query._entities[0]
        if hasattr(entity, "column"):
            col = entity.column
            if query._group_by and query._distinct:
                raise NotImplementedError
            if query._group_by or query._distinct:
                col = distinct(col)
            if query._group_by:
                disable_group_by = True
            count_func = func.count(col)
        else:
            count_func = func.count()
        if query._group_by and not disable_group_by:
            count_func = count_func.over(None)
        count_q = (
            query.options(lazyload("*"))
            .statement.with_only_columns([count_func])
            .order_by(None)
        )
        if disable_group_by:
            count_q = count_q.group_by(None)
        return query.session.execute(count_q).scalar()
