from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.PaymentCategoryResponse])
def read_payment_categories(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve payment categories
    """
    items = crud.payment_category.get_multi_query(db).all()
    return items
