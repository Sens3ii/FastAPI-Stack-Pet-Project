from datetime import date, datetime

from pydantic import BaseModel, PaymentCardNumber, Field
from pydantic.utils import GetterDict

from app.schemas.user import UserNested
from app.utils.constants import TRANSFER_TO_OTHER_FEE
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
    fee: float

    class Config:
        class CustomSchema(GetterDict):
            def get(self, key, default=None):
                if key == 'fee':
                    return 0 if self._obj.kind == CardKind.JUSAN else TRANSFER_TO_OTHER_FEE
                return super().get(key, default)

        orm_mode = True
        getter_dict = CustomSchema


class UserAccountSumRequest(BaseModel):
    sum: float = Field(..., gt=0)


class UserAccountTransferRequest(BaseModel):
    sum: float = Field(..., gt=0)
    card_number: PaymentCardNumber
