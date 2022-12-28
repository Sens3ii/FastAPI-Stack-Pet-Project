from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserNested
from app.utils.enums import TransactionLogKind


class TransactionLogBase(BaseModel):
    sum: int
    user_id: int
    order_id: Optional[int] = None
    recipient_id: Optional[int] = None
    payment_id: Optional[int] = None
    kind: TransactionLogKind

    class Config:
        orm_mode = True


class TransactionLogCreate(TransactionLogBase):
    pass


class TransactionLogUpdate(TransactionLogBase):
    pass


class TransactionLogResponse(BaseModel):
    class OrderNested(BaseModel):
        id: int
        sum: int

        class Config:
            orm_mode = True

    class PaymentNested(BaseModel):
        id: int
        title: str

        class Config:
            orm_mode = True

    class RecipientAccountNested(BaseModel):
        id: int
        card_number: str

        class Config:
            orm_mode = True

    id: int
    sum: int
    kind: TransactionLogKind
    user: UserNested
    order: Optional[OrderNested] = None
    payment: Optional[PaymentNested] = None
    recipient_account: Optional[RecipientAccountNested] = None

    class Config:
        orm_mode = True
