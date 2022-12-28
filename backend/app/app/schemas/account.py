from datetime import date, datetime

from pydantic import BaseModel, PaymentCardNumber

from app.schemas.user import UserNested
from app.utils.enums import CardKind


class UserAccountBase(BaseModel):
    sum: float
    bonuses: float
    card_number: PaymentCardNumber
    expiration_date: date
    kind: CardKind


class UserAccountCreate(UserAccountBase):
    user_id: int


class UserAccountUpdate(UserAccountBase):
    pass


class UserAccountResponse(UserAccountBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserNested

    class Config:
        orm_mode = True


class UserAccountCheckResponse(BaseModel):
    id: int
    card_number: PaymentCardNumber
    kind: CardKind

    class Config:
        orm_mode = True
