from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import PaymentCardNumber
from sqlalchemy.orm import Session

from app import models, crud
from app.api import deps
from app.schemas import UserAccountCheckResponse, UserAccountResponse, UserAccountSumRequest, UserAccountTransferRequest
from app.utils.constants import TRANSFER_TO_OTHER_FEE
from app.utils.enums import CardKind

router = APIRouter()


@router.get("/{card_number}/check/", response_model=UserAccountCheckResponse)
def check_card(
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
        account_in: UserAccountSumRequest
) -> Any:
    """
    Add sum to account
    """
    account = crud.account.get_by_user_id(db, user_id=current_user.id)
    if account is None:
        raise HTTPException(status_code=404, detail="User has no account")
    account = crud.account.add_sum(db, user_account=account, sum=account_in.sum)
    return account


@router.post("/withdraw/", response_model=UserAccountResponse)
def withdraw_sum_from_account(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        account_in: UserAccountSumRequest
) -> Any:
    """
    Add sum to account
    """
    account = crud.account.get_by_user_id(db, user_id=current_user.id)
    if account is None:
        raise HTTPException(status_code=404, detail="User has no account")
    if account_in.sum > account.sum:
        raise HTTPException(status_code=400, detail="Not enough money on account")
    account = crud.account.withdraw_sum(db, user_account=account, sum=account_in.sum)
    return account


@router.post("/transfer/", response_model=UserAccountResponse)
def transfer(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        transfer_in: UserAccountTransferRequest
) -> Any:
    """
    Add sum to account
    """

    account = crud.account.get_by_user_id(db, user_id=current_user.id)
    if account is None:
        raise HTTPException(status_code=404, detail="User has no account")
    recipient_account = crud.account.get_by_card_number(db, card_number=transfer_in.card_number)
    if recipient_account is None:
        raise HTTPException(status_code=400, detail="Recipient Card number not found")
    if current_user.id == recipient_account.user_id:
        raise HTTPException(status_code=400, detail="You can't transfer money to yourself")

    sum_with_fee = transfer_in.sum
    if recipient_account.kind == CardKind.OTHER:
        sum_with_fee = transfer_in.sum + transfer_in.sum * TRANSFER_TO_OTHER_FEE

    if sum_with_fee > account.sum:
        raise HTTPException(status_code=400, detail="Not enough money on account")

    account = crud.account.transfer_sum(db, user_account=account, recipient_account=recipient_account,
                                        sum=transfer_in.sum, sum_with_fee=sum_with_fee)
    return account
