"""Pydantic schemas for cart models"""

from typing import List
from pydantic import BaseModel

from app.schemas.menu import MenuItem

class Cart(BaseModel):
    """Cart entity"""
    id: str
    user_id: str
    restaurant_id: int
    menu_items: List[MenuItem] = []
    total: float = 0.00
