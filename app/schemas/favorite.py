"""Pydantic schema for user favorites."""

from typing import Optional
from pydantic import BaseModel


class Favorite(BaseModel):
    """Favorite entity."""
    id: str
    user_id: str
    restaurant_id: int
    menu_item_id: str
