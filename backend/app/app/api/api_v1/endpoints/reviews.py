from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.ReviewResponse)
def create_review(
        *,
        db: Session = Depends(deps.get_db),
        review_in: schemas.ReviewCreate,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new review.
    """
    if not crud.item.is_purchased(db=db, item_id=review_in.item_id, user_id=current_user.id):
        raise HTTPException(status_code=400, detail="You can't review item that you have not purchased")
    if crud.review.is_reviewed(db=db, item_id=review_in.item_id, user_id=current_user.id):
        raise HTTPException(status_code=400, detail="You have already reviewed this item")
    review = crud.review.create_with_owner(db=db, obj_in=review_in, user_id=current_user.id)
    return review
