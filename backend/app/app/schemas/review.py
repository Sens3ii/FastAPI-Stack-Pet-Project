from pydantic import BaseModel, validator


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
    class UserNested(BaseModel):
        id: int
        email: str
        full_name: str

        class Config:
            orm_mode = True

    id: int
    user: UserNested

    class Config:
        orm_mode = True
