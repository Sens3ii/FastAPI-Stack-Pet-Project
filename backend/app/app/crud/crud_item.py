import random
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, Query

from app.api.filters import ItemFilterParams
from app.crud.base import CRUDBase
from app.models import OrdersItems
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.utils.constants import PURCHASE_BONUS_RANGE


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: ItemCreate, owner_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete(self, db: Session, *, id: int) -> Optional[Item]:
        db_obj = self.get(db, id)
        if not db_obj:
            return None
        db_obj.is_active = False
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def is_purchased(db: Session, *, item_id: int, user_id: int) -> bool:
        if db.query(OrdersItems).filter(OrdersItems.item_id == item_id, OrdersItems.order_user_id == user_id).first():
            return True
        return False

    def get_filtered_query(self, query: Query, filter_params: ItemFilterParams) -> Query:
        if filter_params.category_id:
            query = query.filter(self.model.category_id == filter_params.category_id)
        return query

    def get_by_title(self, db: Session, *, title: str) -> Optional[Item]:
        return db.query(self.model).filter(self.model.title == title).first()

    def create(
            self, db: Session, *, obj_in: ItemCreate,
    ) -> Item:
        bonus_percent = "{:.2f}".format(random.uniform(PURCHASE_BONUS_RANGE[0], PURCHASE_BONUS_RANGE[1]))
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, bonus_percent=bonus_percent)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


item = CRUDItem(Item)
