from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import PaymentCardNumber
from sqlalchemy.orm import Session

from app import models, crud
from app.api import deps
from app.schemas import UserAccountCheckResponse, UserAccountResponse, UserAccountAddSumRequest

router = APIRouter()


@router.get("/{card_number}/check/", response_model=UserAccountCheckResponse)
def read_items(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        card_number: PaymentCardNumber = Path(..., min_length=16, max_length=16)
) -> Any:
    """
    Check card number before transfer
    """

    account = crud.account.get_by_card_number(db, card_number=card_number)
    if account is None:
        raise HTTPException(status_code=400, detail="Card number not found")
    if current_user.id == account.user_id:
        raise HTTPException(status_code=400, detail="You can't transfer money to yourself")
    return account


@router.get("/my/", response_model=UserAccountResponse)
def read_items(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get my account
    """
    account = crud.account.get_by_user_id(db, user_id=current_user.id)
    if account is None:
        raise HTTPException(status_code=404, detail="User has no account")
    return account


@router.post("/add/", response_model=UserAccountResponse)
def add_sum_to_account(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        account_in: UserAccountAddSumRequest
) -> Any:
    """
    Add sum to account
    """
    account = crud.account.get_by_user_id(db, user_id=current_user.id)
    if account is None:
        raise HTTPException(status_code=404, detail="User has no account")
    account = crud.account.add_sum(db, user_account=account, sum=account_in.sum)
    return account
