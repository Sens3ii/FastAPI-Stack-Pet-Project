from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import IsActiveMixin, TimestampMixin


class ItemCategory(Base, TimestampMixin):
    __tablename__ = "item_category"

    title = Column(String)
    items = relationship("Item", back_populates="category")


class Item(Base, IsActiveMixin, TimestampMixin):
    __tablename__ = "item"

    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
    rating = Column(Float)
    reviews = relationship("Review", back_populates="item", order_by="Review.id")
    orders = relationship("OrdersItems", back_populates="item")
    image_url = Column(String(555))
    bonus_percent = Column(Float, default=0.0)
    category_id = Column(Integer, ForeignKey("item_category.id"))
    category = relationship("ItemCategory", back_populates="items")
