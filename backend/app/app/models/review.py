from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Review(Base, TimestampMixin):
    __tablename__ = "review"

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    comment = Column(String, index=True)
    rating = Column(Float)
    item_id = Column(Integer, ForeignKey("item.id"))
    item = relationship("Item", back_populates="reviews")
