from pydantic import BaseModel


class PaymentCategoryBase(BaseModel):
    title: str


class PaymentCategoryCreate(PaymentCategoryBase):
    pass


class PaymentCategoryUpdate(PaymentCategoryBase):
    pass


class PaymentCategoryResponse(PaymentCategoryBase):
    id: int

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    title: str
    category_id: int


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int

    class Config:
        orm_mode = True
