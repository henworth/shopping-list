from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ShoppingItem
from app.schemas import ShoppingItemCreate, ShoppingItemUpdate


def create_item(db: Session, payload: ShoppingItemCreate) -> ShoppingItem:
    item = ShoppingItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item(db: Session, item_id: int) -> ShoppingItem | None:
    return db.get(ShoppingItem, item_id)


def list_items(db: Session, *, purchased: bool | None = None) -> list[ShoppingItem]:
    stmt = select(ShoppingItem)
    if purchased is not None:
        stmt = stmt.where(ShoppingItem.purchased == purchased)
    return list(db.scalars(stmt.order_by(ShoppingItem.id.desc())))


def update_item(
    db: Session, item: ShoppingItem, payload: ShoppingItemUpdate
) -> ShoppingItem:
    data = payload.model_dump(exclude_unset=True)
    if "purchased" in data and data["purchased"] and not item.purchased:
        item.purchased_at = datetime.now(timezone.utc)
    for field, value in data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def mark_purchased(db: Session, item: ShoppingItem) -> ShoppingItem:
    item.purchased = True
    item.purchased_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, item: ShoppingItem) -> None:
    db.delete(item)
    db.commit()
