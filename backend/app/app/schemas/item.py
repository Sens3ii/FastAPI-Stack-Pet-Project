from typing import Optional

from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    title: str
    description: str
    price: int


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


class ItemResponse(ItemBase):
    class OwnerNested(BaseModel):
        id: int
        email: str
        full_name: str

        class Config:
            orm_mode = True

    id: int
    rating: Optional[float] = None
    owner: OwnerNested

    class Config:
        orm_mode = True
