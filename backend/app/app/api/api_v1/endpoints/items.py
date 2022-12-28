from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ItemResponse])
def read_items(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        rating_above: Optional[float] = Query(None, ge=0, le=5),
        rating_below: Optional[float] = Query(None, ge=0, le=5),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve items.
    """

    items = crud.item.get_filtered_items(db, skip=skip, limit=limit, search=search, rating_above=rating_above,
                                         rating_below=rating_below)
    return items


# @router.get("/my/", response_model=List[schemas.ItemResponse])
def read_items_by_user(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        rating_above: Optional[float] = Query(None, ge=0, le=5),
        rating_below: Optional[float] = Query(None, ge=0, le=5),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve items.
    """

    items = crud.item.get_filtered_items(db, skip=skip, limit=limit, search=search, rating_above=rating_above,
                                         rating_below=rating_below, owner_id=current_user.id)
    return items


# @router.post("/", response_model=schemas.ItemResponse)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.ItemCreate,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new item.
    """
    if crud.user.is_admin(db, user=current_user) or crud.user.is_seller(db, user=current_user):
        item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return item


# @router.put("/{id}/", response_model=schemas.ItemResponse)
def update_item(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        item_in: schemas.ItemUpdate,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_admin(db, user=current_user) and not crud.user.is_seller(db, user=current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not crud.user.is_admin(db, user=current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}/", response_model=schemas.ItemResponse)
def read_item(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/{id}/reviews/", response_model=list[schemas.ReviewResponse])
def read_item_reviews(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    reviews = crud.review.get_multi_by_item_id(db=db, item_id=id)
    return reviews


# @router.delete("/{id}", response_model=schemas.ItemResponse)
def delete_item(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_admin(db, user=current_user) and not crud.user.is_seller(db, user=current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not crud.user.is_admin(db, user=current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = crud.item.delete(db=db, id=id)
    return item
