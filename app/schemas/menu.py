"""Pydantic schemas for menu models"""

from typing import List
from pydantic import BaseModel

class MenuItem(BaseModel):
    """Menu entity."""
    id: str
    name: str
    price: float
    description: str
    tags: List[str] = []

class CreateMenuItem(BaseModel):
    """Menu entity."""
    name: str
    price: float
    description: str
    tags: List[str] = []
