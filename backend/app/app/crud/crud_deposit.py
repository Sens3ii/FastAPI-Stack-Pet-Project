from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models.deposit import UserDeposit
from app.schemas import UserDepositCreate, UserDepositUpdate


class CRUDUserDeposit(CRUDBase[UserDeposit, UserDepositCreate, UserDepositUpdate]):

    def generate_user_deposit(self, db: Session, *, user_id: int):
        db_obj = self.model(user_id=user_id, sum=0)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_id(self, db: Session, *, user_id: int) -> UserDeposit:
        return db.query(self.model).filter(self.model.user_id == user_id).first()

    def add_sum(self, db: Session, *, user_deposit: UserDeposit, sum: float) -> UserDeposit:
        crud.account.withdraw_sum(db, user_account=user_deposit.user.account, sum=sum)
        user_deposit.sum += sum
        db.add(user_deposit)
        db.commit()
        db.refresh(user_deposit)
        return user_deposit

    def withdraw_sum(self, db: Session, *, user_deposit: UserDeposit, sum: float) -> UserDeposit:
        crud.account.add_sum(db, user_account=user_deposit.user.account, sum=sum)
        return self.add_sum(db, user_deposit=user_deposit, sum=-sum)


deposit = CRUDUserDeposit(UserDeposit)
