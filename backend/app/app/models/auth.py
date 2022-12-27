from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy import Enum as EnumType
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql.functions import concat

from app.db.base_class import Base
from app.models.mixins import IsActiveMixin, TimestampMixin
from app.utils.enums import Gender


class User(Base, IsActiveMixin, TimestampMixin):
    __tablename__ = "user"

    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(50), nullable=False)
    hashed_password = Column(String, nullable=False)
    gender = Column(EnumType(Gender))
    first_name = Column(String(555))
    last_name = Column(String(555))
    full_name = column_property(concat(first_name, " ", last_name))
    birth_date = Column(Date)
    items = relationship("Item", back_populates="owner", order_by="Item.id")
    roles = relationship("UsersRoles", back_populates="user", order_by="UsersRoles.role_id")
    orders = relationship("Order", back_populates="user", order_by="Order.id")


class Role(Base):
    __tablename__ = "role"

    name = Column(String(255))
    codename = Column(String(128))
    users = relationship("UsersRoles", back_populates="role")


class UsersRoles(Base):
    __tablename__ = "users_roles"

    id = None
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    user = relationship("User", back_populates="roles", order_by="User.id")
    role_id = Column(ForeignKey("role.id"), primary_key=True)
    role = relationship("Role", back_populates="users", order_by="Role.id ")

    role_name = association_proxy(target_collection="role", attr="name")
    role_codename = association_proxy(target_collection="role", attr="codename")
