from pydantic import BaseModel, validator

from app.schemas.user import UserNested


class ReviewBase(BaseModel):
    comment: str
    rating: int


class ReviewCreate(ReviewBase):
    item_id: int

    @validator('rating')
    def rating_must_be_between_1_and_5(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v


class ReviewUpdate(ReviewBase):

    @validator('rating')
    def rating_must_be_between_1_and_5(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v


class ReviewResponse(ReviewBase):
    id: int
    user: UserNested

    class Config:
        orm_mode = True
