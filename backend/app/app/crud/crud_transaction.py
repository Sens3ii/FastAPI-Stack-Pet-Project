from sqlalchemy.orm import Query

from app.crud.base import CRUDBase
from app.models import TransactionLog
from app.schemas import TransactionLogCreate, TransactionLogUpdate


class CRUDTransactionLog(CRUDBase[TransactionLog, TransactionLogCreate, TransactionLogUpdate]):

    def get_multi_query_by_user_id(self, db, *, user_id: int):
        return db.query(self.model).filter(TransactionLog.user_id == user_id)

    def get_filtered_query(self, query: Query, filter_params: object) -> Query:
        if filter_params:
            for key, value in filter_params.__dict__.items():
                if value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        return query


transaction_log = CRUDTransactionLog(TransactionLog)
