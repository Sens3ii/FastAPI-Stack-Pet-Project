from typing import Optional

from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    """Base class for order schema"""
    address: str


class OrderCreate(OrderBase):
    item_ids: list[int] = Field(..., min_items=1)


class OrderUpdate(BaseModel):
    status: str


class OrderResponse(OrderBase):
    class Item(BaseModel):
        item_id: Optional[int] = Field(None, alias="item_id")
        item_title: Optional[str] = Field(None, alias="item_title")
        item_price: Optional[int] = Field(None, alias="item_price")

        class Config:
            orm_mode = True
            allow_population_by_field_name = True

    """Response class for order schema"""
    id: int
    status: Optional[str] = Field(None)
    items: Optional[list[Item]] = Field(None)

    class Config:
        orm_mode = True
