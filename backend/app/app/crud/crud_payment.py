from sqlalchemy.orm import Query

from app import crud
from app.api.filters import ItemFilterParams
from app.crud.base import CRUDBase
from app.models import Payment, User
from app.schemas import PaymentCreate, PaymentUpdate, PaymentPayRequest, TransactionLogCreate
from app.utils.constants import PAYMENT_BONUS_FINAL_CONSTRAINT, PAYMENT_BONUS_FINAL, \
    PAYMENT_BONUS_INITIAL
from app.utils.enums import TransactionLogKind


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def get_by_title(self, db, *, title: str) -> Payment:
        return db.query(self.model).filter(self.model.title == title).first()

    def get_filtered_query(self, query: Query, filter_params: ItemFilterParams) -> Query:
        if filter_params.category_id:
            query = query.filter(self.model.category_id == filter_params.category_id)
        return query

    @staticmethod
    def pay(db, *, user: User, payment_in: PaymentPayRequest):
        sum, payment_id = payment_in.sum, payment_in.payment_id
        account = crud.account.get_by_user_id(db, user_id=user.id)
        if account.sum >= PAYMENT_BONUS_FINAL_CONSTRAINT:
            bonus_percent = PAYMENT_BONUS_FINAL
        else:
            bonus_percent = PAYMENT_BONUS_INITIAL
        bonus = sum * bonus_percent
        crud.account.add_bonuses(db, user_account=account, sum=bonus)
        crud.account.withdraw_sum(db, user_account=account, sum=sum)
        crud.transaction_log.create(db, obj_in=TransactionLogCreate(
            user_id=user.id,
            sum=sum,
            payment_id=int(payment_id),
            kind=TransactionLogKind.PAYMENT,
        ))


payment = CRUDPayment(Payment)
