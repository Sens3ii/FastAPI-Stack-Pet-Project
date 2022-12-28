from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Order(Base, TimestampMixin):
    __tablename__ = "order"

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    sum = Column(Integer)
    items = relationship("OrdersItems", back_populates="order", order_by="OrdersItems.item_id")
    transaction_log = relationship("TransactionLog", back_populates="order", uselist=False)


class OrdersItems(Base):
    __tablename__ = "orders_items"

    id = None
    order_id = Column(ForeignKey("order.id"), primary_key=True)
    order = relationship("Order", back_populates="items", order_by="Order.id")
    item_id = Column(ForeignKey("item.id"), primary_key=True)
    item = relationship("Item", back_populates="orders", order_by="Item.id")
    quantity = Column(Integer)
    sum = Column(Integer)

    item_title = association_proxy(target_collection="item", attr="title")
    item_price = association_proxy(target_collection="item", attr="price")
