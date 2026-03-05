"""Pydantic schemas for cart models"""

from typing import List
from pydantic import BaseModel

from app.schemas.menu import MenuItem

class CartItem(BaseModel):
    """CartItem entity"""
    item: MenuItem
    quantity: int

class Cart(BaseModel):
    """Cart entity"""
    id: str
    user_id: str
    restaurant_id: int
    cart_items: List[CartItem] = []
    subtotal: float = 0.00
    tax: float = 0.00
    total: float = 0.00
