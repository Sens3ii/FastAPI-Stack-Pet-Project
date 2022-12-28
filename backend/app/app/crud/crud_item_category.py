from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import ItemCategory
from app.schemas import ItemCategoryCreate, ItemCategoryUpdate


class CRUDItemCategory(CRUDBase[ItemCategory, ItemCategoryCreate, ItemCategoryUpdate]):

    def get_by_title(self, db: Session, *, title: str) -> Optional[ItemCategory]:
        return db.query(self.model).filter(self.model.title == title).first()


item_category = CRUDItemCategory(ItemCategory)
