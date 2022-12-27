from sqlalchemy import TIMESTAMP, Boolean, Column, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:
    __abstract__ = True

    __created_at_name__ = "created_at"
    __updated_at_name__ = "updated_at"
    __datetime_func__ = func.now()

    created_at = Column(
        __created_at_name__,
        TIMESTAMP(timezone=True),
        default=__datetime_func__,
        nullable=False,
        doc="Дата создания",
    )

    updated_at = Column(
        __updated_at_name__,
        TIMESTAMP(timezone=True),
        default=__datetime_func__,
        onupdate=__datetime_func__,
        nullable=False,
        doc="Дата обновления",
    )


@declarative_mixin
class IsActiveMixin:
    __abstract__ = True

    is_active = Column(Boolean, nullable=False, default=True)
