from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.utils.enums import Gender


class UserBase(BaseModel):
    email: EmailStr
    phone: str
    first_name: str
    last_name: str
    gender: Gender
    birth_date: date = Field(..., example="2000-01-01")
    avatar_url: Optional[str] = None


class UserRegistration(UserBase):
    password: str


class UserCreate(UserBase):
    password: str
    role_code: str


class UserUpdate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    role_code: str

    class Config:
        orm_mode = True


class UserNested(BaseModel):
    id: int
    email: str
    full_name: str
    avatar_url: Optional[str] = None

    class Config:
        orm_mode = True
