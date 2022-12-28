from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import OrdersItems
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


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

    def get_filtered_items(self, db: Session, *, skip: int = 0, limit: int = 100, search: Optional[str] = None,
                           rating_above: Optional[float], rating_below: Optional[float],
                           owner_id: Optional[int] = None) -> \
            list[Item]:
        query = db.query(self.model).filter(self.model.is_active == True)
        if search:
            query = query.filter(self.model.title.contains(search))
        if rating_above:
            query = query.filter(self.model.rating >= rating_above)
        if rating_below:
            query = query.filter(self.model.rating <= rating_below)
        if owner_id:
            query = query.filter(self.model.owner_id == owner_id)
        query = query.offset(skip).limit(limit)
        return query.all()

    @staticmethod
    def is_purchased(self, db: Session, *, item_id: int, user_id: int) -> bool:
        if db.query(OrdersItems).filter(OrdersItems.item_id == item_id, OrdersItems.user_id == user_id).first():
            return True
        return False


item = CRUDItem(Item)
