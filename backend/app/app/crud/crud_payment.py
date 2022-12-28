from sqlalchemy.orm import Query

from app.api.filters import ItemFilterParams
from app.crud.base import CRUDBase
from app.models import Payment
from app.schemas import PaymentCreate, PaymentUpdate


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def get_by_title(self, db, *, title: str) -> Payment:
        return db.query(self.model).filter(self.model.title == title).first()

    def get_filtered_query(self, query: Query, filter_params: ItemFilterParams) -> Query:
        if filter_params.category_id:
            query = query.filter(self.model.category_id == filter_params.category_id)
        return query


payment = CRUDPayment(Payment)
