from pydantic import BaseModel

from app.schemas.user import UserNested


class UserDepositBase(BaseModel):
    sum: float


class UserDepositCreate(UserDepositBase):
    user_id: int


class UserDepositUpdate(UserDepositBase):
    pass


class UserDepositResponse(UserDepositBase):
    id: int
    user: UserNested

    class Config:
        orm_mode = True
