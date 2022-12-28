from typing import Optional

from pydantic import BaseModel, Field

from app.utils.enums import OrderType


class OrderSchema(BaseModel):
    field: Optional[str] = Field(None, title="Поле для сортировки", max_length=128)
    type: Optional[OrderType] = Field(
        None, title="Тип сортировки. По возрастанию или убыванию", max_length=4
    )


class ResponseBase(BaseModel):
    message: str = Field(..., example="some message")


class ErrorResponse(ResponseBase):
    errors: dict = Field(
        ..., example={"field_name1": "error message", "field_name2": "error message"}
    )
