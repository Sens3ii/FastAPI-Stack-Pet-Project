from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.OrderResponse)
def create_order(
        *,
        db: Session = Depends(deps.get_db),
        order_in: schemas.OrderCreate,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new order.
    """
    order = crud.order.create_order(db=db, obj_in=order_in, user_id=current_user.id)
    return order


@router.get("/", response_model=list[schemas.OrderResponse])
def read_orders(
        *,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve orders.
    """
    orders = crud.order.get_multi(db=db, skip=skip, limit=limit)
    return orders


@router.get("/my", response_model=list[schemas.OrderResponse])
def read_my_orders(
        *,
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve my orders.
    """
    orders = crud.order.get_multi_by_owner(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return orders
