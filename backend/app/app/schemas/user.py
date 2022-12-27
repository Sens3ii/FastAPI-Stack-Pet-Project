from datetime import date

from pydantic import BaseModel, EmailStr, Field

from app.utils.enums import Gender


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    phone: str
    first_name: str
    last_name: str
    gender: Gender
    birth_date: date = Field(..., example="2000-01-01")


class UserRegistration(UserBase):
    password: str


class UserCreate(UserBase):
    password: str
    role_code: str


class UserUpdate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
