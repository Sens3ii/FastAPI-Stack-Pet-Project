from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Order, Item, OrdersItems
from app.schemas import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_multi_by_owner(
            self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Item]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def assign_items(db: Session, item_ids: Optional[list[int]], order_id: int):
        for item_id in item_ids:
            db.add(OrdersItems(item_id=item_id, order_id=order_id))

    def create_order(self, db: Session, *, obj_in: OrderCreate, user_id: int) -> Order:
        item_ids = obj_in.item_ids
        del obj_in.item_ids
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        self.assign_items(db, item_ids=item_ids, order_id=db_obj.id)
        db.commit()
        db.refresh(db_obj)
        return db_obj


order = CRUDOrder(Order)
