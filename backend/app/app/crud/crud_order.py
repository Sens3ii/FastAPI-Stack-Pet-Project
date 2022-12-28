from typing import Optional

from sqlalchemy.orm import Session, Query

from app import crud
from app.crud.base import CRUDBase
from app.models import Order, OrdersItems
from app.schemas import OrderCreate, OrderUpdate, OrderRequest, OrderItemCreate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_multi_query_by_user_id(self, db: Session, *, user_id: int) -> Query:
        return self.get_multi_query(db).filter(self.model.user_id == user_id)

    @staticmethod
    def assign_items(db: Session, items: Optional[list[OrderItemCreate]], order_id: int):
        for item in items:
            db.add(OrdersItems(**item.dict()))

    def create_order(self, db: Session, *, obj_in: OrderRequest, user_id: int) -> Order:
        # creating order
        db_obj = self.model(user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # init items
        items = obj_in.items
        items_with_sum = []
        total_sum = 0
        for item in items:
            item_orm = crud.item.get(db=db, id=item.item_id)
            if item_orm:
                item_sum = item_orm.price * item.quantity
                total_sum += item_sum
                items_with_sum.append(
                    OrderItemCreate(item_id=item_orm.id, quantity=item.quantity, sum=item_sum, order_id=db_obj.id))
        # add sum order
        db_obj.sum = total_sum
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # create order item relation
        self.assign_items(db, items=items_with_sum, order_id=db_obj.id)
        db.commit()
        db.refresh(db_obj)
        return db_obj


order = CRUDOrder(Order)
