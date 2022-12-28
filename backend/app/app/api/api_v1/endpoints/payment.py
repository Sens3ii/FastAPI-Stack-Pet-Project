from typing import Any

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.api.filters import ItemFilterParams

router = APIRouter()


@router.get("/", response_model=Page[schemas.PaymentResponse])
def read_payments(
        db: Session = Depends(deps.get_db),
        filter_in: ItemFilterParams = Depends(),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve payments.
    """
    query = crud.payment.get_multi_query(db)
    query = crud.payment.get_filtered_query(query=query, filter_params=filter_in)
    payment = crud.item.get_paginated(query)
    return payment
