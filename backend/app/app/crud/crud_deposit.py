from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.deposit import UserDeposit
from app.schemas import UserDepositCreate, UserDepositUpdate


class CRUDUserDeposit(CRUDBase[UserDeposit, UserDepositCreate, UserDepositUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> UserDeposit:
        return db.query(self).filter(UserDeposit.user_id == user_id).first()

    def add_sum(self, db: Session, *, user_id: int, sum: float) -> UserDeposit:
        user_deposit = self.get_by_user_id(db, user_id=user_id)
        user_deposit.sum += sum
        db.commit()
        db.refresh(user_deposit)
        return user_deposit
