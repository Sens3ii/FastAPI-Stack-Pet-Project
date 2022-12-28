from typing import Generator
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi import Query
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas import OrderSchema
from app.utils.enums import OrderType

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_admin_user(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_admin(db=db, user=current_user):
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


class OrderParams:
    def __init__(self, available_fields: list[str]):
        self.available_fields = available_fields

    def __call__(
            self,
            order: Optional[str] = Query(
                default=None,
                max_length=128,
                title="Order field",
                description="{field_name} - ascending order\n\n"
                            "-{field_name} - descending order",
            ),
    ) -> Optional[OrderSchema]:
        if order and len(order) != 0:
            type_ = OrderType.ASC
            field = order
            if order[0] == "-":
                type_ = OrderType.DESC
                field = order[1:]
            if field in self.available_fields:
                return OrderSchema(field=field, type=type_)
        return None
