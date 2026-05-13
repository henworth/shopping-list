from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import Priority


class ShoppingItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str | None = Field(default=None, max_length=60)
    quantity: float = Field(default=1.0, ge=0)
    unit: str = Field(default="pcs", max_length=20)
    priority: Priority = Priority.medium
    notes: str | None = Field(default=None, max_length=500)


class ShoppingItemCreate(ShoppingItemBase):
    pass


class ShoppingItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    category: str | None = Field(default=None, max_length=60)
    quantity: float | None = Field(default=None, ge=0)
    unit: str | None = Field(default=None, max_length=20)
    priority: Priority | None = None
    notes: str | None = Field(default=None, max_length=500)
    purchased: bool | None = None


class ShoppingItemRead(ShoppingItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    purchased: bool
    purchased_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PantryItemPayload(BaseModel):
    """Payload sent to the pantry service when a shopping item is marked purchased."""

    name: str
    category: str | None = None
    quantity: float
    unit: str
    notes: str | None = None
