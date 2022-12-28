from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import Enum as EnumType
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin
from app.utils.enums import TransactionLogKind


class TransactionLog(Base, TimestampMixin):
    __tablename__ = "transaction_log"

    sum = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    order_id = Column(Integer, ForeignKey("order.id"), nullable=True)
    order = relationship("Order", back_populates="transaction_log")
    user = relationship("User", back_populates="transaction_logs")
    recipient_account_id = Column(Integer, ForeignKey("user_account.id"), nullable=True)
    recipient_account = relationship("UserAccount", back_populates="transaction_logs")
    payment_id = Column(Integer, ForeignKey("payment.id"), nullable=True)
    payment = relationship("Payment", back_populates="transaction_logs")
    kind = Column(EnumType(TransactionLogKind), nullable=True)
