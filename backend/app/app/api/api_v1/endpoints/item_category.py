from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.ItemCategoryResponse])
def read_item_categories(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve item categories
    """
    items = crud.item_category.get_multi_query(db).all()
    return items
