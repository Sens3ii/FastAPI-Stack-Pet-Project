from app.crud.base import CRUDBase
from app.models import TransactionLog
from app.schemas import TransactionLogCreate, TransactionLogUpdate


class CRUDTransactionLog(CRUDBase[TransactionLog, TransactionLogCreate, TransactionLogUpdate]):
    def get_by_user_id(self, db, *, user_id: int):
        return db.query(self).filter(TransactionLog.user_id == user_id).all()
