from datetime import date, timedelta

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models import UserAccount
from app.schemas import UserAccountCreate, UserAccountUpdate, TransactionLogCreate
from app.utils.account import generate_card_number
from app.utils.enums import CardKind, TransactionLogKind


class CRUDUserAccount(CRUDBase[UserAccount, UserAccountCreate, UserAccountUpdate]):
    def generate_user_account(
            self, db: Session, *, user_id: int
    ) -> UserAccount:
        obj_in_data = jsonable_encoder(UserAccountCreate(
            user_id=user_id,
            sum=0,
            bonuses=0,
            card_number=generate_card_number('4111'),
            expiration_date=date.today() + timedelta(days=4 * 365),
            kind=CardKind.JUSAN,
        ))
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user_id(self, db: Session, *, user_id: int) -> UserAccount:
        return (
            db.query(self.model)
            .filter(UserAccount.user_id == user_id)
            .first()
        )

    def get_by_card_number(self, db: Session, *, card_number: str) -> UserAccount:
        return (
            db.query(self.model)
            .filter(UserAccount.card_number == card_number)
            .first()
        )

    def add_sum(self, db: Session, *, user_account: UserAccount, sum: float) -> UserAccount:
        user_account.sum += sum
        db.add(user_account)
        db.commit()
        db.refresh(user_account)
        return user_account

    def add_bonuses(self, db: Session, *, user_account: UserAccount, sum: float) -> UserAccount:
        user_account.bonuses += sum
        db.add(user_account)
        db.commit()
        db.refresh(user_account)
        return user_account

    def withdraw_sum(self, db: Session, *, user_account: UserAccount, sum: float) -> UserAccount:
        return self.add_sum(db, user_account=user_account, sum=-sum)

    def transfer_sum(
            self, db: Session, *, user_account: UserAccount, recipient_account: UserAccount, sum: float,
            sum_with_fee: float
    ) -> UserAccount:
        crud.transaction_log.create(db, obj_in=TransactionLogCreate(user_id=user_account.user_id,
                                                                    sum=sum,
                                                                    kind=TransactionLogKind.TRANSFER,
                                                                    recipient_account_id=recipient_account.id,
                                                                    ))
        self.add_sum(db, user_account=recipient_account, sum=sum)
        self.withdraw_sum(db, user_account=user_account, sum=sum_with_fee)
        return user_account


account = CRUDUserAccount(UserAccount)
