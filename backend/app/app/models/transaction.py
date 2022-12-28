from sqlalchemy import Enum as EnumType

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin
from app.utils.enums import TransactionLogKind


class TransactionLog(Base, TimestampMixin):
    __tablename__ = "transaction_log"

    sum = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    item_id = Column(Integer, ForeignKey("item.id"), nullable=True)
    item = relationship("Item", back_populates="transaction_logs")
    user = relationship("User", back_populates="transaction_logs")
    recipient_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    recipient = relationship("User", back_populates="transaction_logs")
    payment_id = Column(Integer, ForeignKey("payment.id"), nullable=True)
    payment = relationship("Payment", back_populates="transaction_logs")
    kind = Column(EnumType(TransactionLogKind), nullable=True)
