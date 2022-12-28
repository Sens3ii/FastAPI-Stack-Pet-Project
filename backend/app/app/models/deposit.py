from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class UserDeposit(Base, TimestampMixin):
    __tablename__ = 'user_deposit'

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='deposit')
    sum = Column(Float, default=0.0)
