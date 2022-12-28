from typing import Any

from fastapi import APIRouter, Depends, HTTPException
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


@router.post("/pay/", response_model=schemas.UserAccountResponse)
def pay(
        *,
        db: Session = Depends(deps.get_db),
        payment_in: schemas.PaymentPayRequest,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Pay.
    """
    account = crud.account.get_by_user_id(db, user_id=current_user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.sum < payment_in.sum:
        raise HTTPException(status_code=400, detail="Not enough money")
    payment = crud.payment.get(db, id=payment_in.payment_id)
    if not payment:
        raise HTTPException(status_code=400, detail="Payment not found")
    crud.payment.pay(db=db, user=current_user, payment_in=payment_in)
    return account
