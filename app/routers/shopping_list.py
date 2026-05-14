from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.clients.pantry import PantryServiceError, create_pantry_item
from app.database import get_db
from app.schemas import (
    PantryItemPayload,
    ShoppingItemCreate,
    ShoppingItemRead,
    ShoppingItemUpdate,
)

router = APIRouter(prefix="/lists", tags=["lists"])


@router.post(path="", response_model=ShoppingItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ShoppingItemCreate, db: Session = Depends(get_db)) -> ShoppingItemRead:
    return ShoppingItemRead.model_validate(crud.create_item(db, payload))


@router.get(path="", response_model=list[ShoppingItemRead])
def list_items(
    purchased: bool | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[ShoppingItemRead]:
    items = crud.list_items(db, purchased=purchased)
    return [ShoppingItemRead.model_validate(i) for i in items]


@router.get(path="/{item_id}", response_model=ShoppingItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ShoppingItemRead:
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="shopping item not found")
    return ShoppingItemRead.model_validate(item)


@router.patch(path="/{item_id}", response_model=ShoppingItemRead)
def update_item(item_id: int, payload: ShoppingItemUpdate, db: Session = Depends(get_db)) -> ShoppingItemRead:
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="shopping item not found")
    return ShoppingItemRead.model_validate(crud.update_item(db, item, payload))


@router.delete(path="/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="shopping item not found")
    crud.delete_item(db, item)


@router.post(path="/{item_id}/purchase", response_model=ShoppingItemRead)
def purchase_item(item_id: int, db: Session = Depends(get_db)) -> ShoppingItemRead:
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="shopping item not found")
    if item.purchased:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already purchased")

    payload = PantryItemPayload(
        name=item.name,
        category=item.category,
        quantity=item.quantity,
        unit=item.unit,
        notes=f"from shopping list #{item.id}",
    )
    try:
        create_pantry_item(payload)
    except PantryServiceError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return ShoppingItemRead.model_validate(crud.mark_purchased(db, item))
