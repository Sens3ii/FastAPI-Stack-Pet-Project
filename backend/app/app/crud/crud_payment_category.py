from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import PaymentCategory
from app.schemas import PaymentCategoryCreate, PaymentCategoryUpdate


class CRUDPaymentCategory(CRUDBase[PaymentCategory, PaymentCategoryCreate, PaymentCategoryUpdate]):
    def get_by_title(self, db: Session, *, title: str) -> Optional[PaymentCategory]:
        return db.query(self.model).filter(PaymentCategory.title == title).first()


payment_category = CRUDPaymentCategory(PaymentCategory)
