from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class PaymentCategory(Base, TimestampMixin):
    __tablename__ = "payment_category"

    title = Column(String)
    payments = relationship("Payment", back_populates="category", order_by="Payment.id")


class Payment(Base, TimestampMixin):
    __tablename__ = "payment"

    title = Column(String)
    category_id = Column(Integer, ForeignKey("payment_category.id"))
    category = relationship("PaymentCategory", back_populates="payments")
    transaction_logs = relationship("TransactionLog", back_populates="payment", order_by="TransactionLog.id")
