from typing import Any

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

from app import schemas, crud, models
from app.api import deps
from app.api.filters import TransactionFilterParams

router = APIRouter()


@router.get("/my/", response_model=Page[schemas.TransactionLogResponse])
def read_my_transactions(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        filter_in: TransactionFilterParams = Depends(),
) -> Any:
    """
    Retrieve transactions.
    """
    query = crud.transaction_log.get_multi_query_by_user_id(db=db, user_id=current_user.id)
    query = crud.transaction_log.get_filtered_query(query=query, filter_params=filter_in)
    transactions = crud.transaction_log.get_paginated(query=query)
    return transactions
