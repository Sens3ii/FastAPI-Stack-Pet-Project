from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy import Enum as EnumType, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin
from app.utils.enums import CardKind


class UserAccount(Base, TimestampMixin):
    __tablename__ = 'user_account'

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='account')
    sum = Column(Float, default=0.0)
    bonuses = Column(Float, default=0.0)
    card_number = Column(String(16), nullable=False)
    kind = Column(EnumType(CardKind), nullable=False, default=CardKind.JUSAN)
    expiration_date = Column(Date, nullable=False)
