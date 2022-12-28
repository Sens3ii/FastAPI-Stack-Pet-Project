from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, crud
from app.api import deps
from app.schemas import UserDepositResponse, UserDepositSumRequest

router = APIRouter()


@router.get("/my/", response_model=UserDepositResponse)
def read_my_deposit(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get my deposit
    """
    deposit = crud.deposit.get_by_user_id(db, user_id=current_user.id)
    if deposit is None:
        raise HTTPException(status_code=404, detail="User has no deposit")
    return deposit


@router.post("/add/", response_model=UserDepositResponse)
def add_sum_to_deposit(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        deposit_in: UserDepositSumRequest
) -> Any:
    """
    Add sum to deposit
    """
    deposit = crud.deposit.get_by_user_id(db, user_id=current_user.id)
    if deposit is None:
        raise HTTPException(status_code=404, detail="User has no deposit")
    account = crud.account.get_by_user_id(db, user_id=current_user.id)
    if account is None:
        raise HTTPException(status_code=404, detail="User has no account")
    if deposit_in.sum > account.sum:
        raise HTTPException(status_code=400, detail="Not enough money on account")
    deposit = crud.deposit.add_sum(db, user_deposit=deposit, sum=deposit_in.sum)
    return deposit


@router.post("/withdraw/", response_model=UserDepositResponse)
def withdraw_sum_from_deposit(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        deposit_in: UserDepositSumRequest
) -> Any:
    """
    Add sum to deposit
    """
    deposit = crud.deposit.get_by_user_id(db, user_id=current_user.id)
    if deposit is None:
        raise HTTPException(status_code=404, detail="User has no deposit")
    if deposit_in.sum > deposit.sum:
        raise HTTPException(status_code=400, detail="Not enough money on deposit")
    deposit = crud.deposit.withdraw_sum(db, user_deposit=deposit, sum=deposit_in.sum)
    return deposit
