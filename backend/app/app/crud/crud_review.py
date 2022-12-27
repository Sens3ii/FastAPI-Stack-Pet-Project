from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Review
from app.schemas import ReviewCreate, ReviewUpdate


class CRUDReview(CRUDBase[Review, ReviewCreate, ReviewUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: ReviewCreate, user_id: int
    ) -> Review:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_item_id(self, db: Session, *, item_id: int) -> list[Review]:
        return db.query(self.model).filter(self.model.item_id == item_id).all()


review = CRUDReview(Review)
