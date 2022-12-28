from typing import Optional

from pydantic import BaseModel


# Shared properties
class ItemBase(BaseModel):
    title: str
    description: str
    price: int
    image_url: Optional[str] = None
    category_id: int


# Properties to receive on item creation
class ItemCreate(ItemBase):
    owner_id: int


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
    bonus_percent: float

    class Config:
        orm_mode = True


class ItemCategoryBase(BaseModel):
    title: str


class ItemCategoryCreate(ItemCategoryBase):
    pass


class ItemCategoryUpdate(ItemCategoryBase):
    pass


class ItemCategoryResponse(ItemCategoryBase):
    id: int

    class Config:
        orm_mode = True
