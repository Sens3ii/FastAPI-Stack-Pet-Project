from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import or_, text
from sqlalchemy.orm import Session, Query

from app.db.base_class import Base
from app.schemas.base import OrderSchema

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get_multi_query(self, db: Session) -> Query:
        """
        Get multiple ORM-level SQL construction object
        """
        return db.query(self.model).order_by(self.model.id.desc())

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Return the first result or None if the result doesn't contain any row
        """
        query = self.get_multi_query(db=db).filter(self.model.id == id)
        return query.first()

    def get_filtered_query(self, query: Query, filter_params: object) -> Query:
        """
        Filter query by filter params
        Override this function in your CRUD model
        """
        return query

    def get_query_by_search_value(
            self, query: Query, value: Optional[str], search_fields: list[str]
    ) -> Query:
        """
        Filter query by search key and list of fields
        """
        if not value:
            return query
        return query.filter(
            or_(
                getattr(self.model, col_name).ilike("%" + value + "%")
                for col_name in search_fields
            )
        )

    def get_ordered_query(self, query: Query, order_params: Optional[OrderSchema]):
        if order_params:
            query = query.order_by(None).order_by(
                text(
                    f"{self.model.__tablename__}.{order_params.field} {order_params.type}"
                )
            )
        return query

    def get_multi(self, db: Session) -> AbstractPage:
        return paginate(self.get_multi_query(db))

    @staticmethod
    def get_paginated(self, query: Query) -> AbstractPage:
        return paginate(query)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def is_exist(self, db: Session, data: Optional[Union[list[int], int]]) -> bool:
        """
        Function that checks if objects exist by list of ids or id
        """
        if isinstance(data, list):
            query_count = (
                db.query(self.model.id).filter(self.model.id.in_(data)).count()
            )
            return query_count == len(data)
        q = db.query(self.model.id).filter(self.model.id == data)
        is_exists = db.query(q.exists()).scalar()
        return is_exists
