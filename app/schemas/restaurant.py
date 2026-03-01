"""Pydantic schemas for restaurant data models."""

from typing import List
from pydantic import BaseModel
from app.schemas.menu import MenuItem

class Restaurant(BaseModel):
    """Restaurant entity."""
    id: int
    name: str
    hours: dict[str, str]
    phone_number: str
    address: str
    tags: List[str] = []
    menu: List[MenuItem] = []

class UpdateRestaurant(BaseModel):
    """Update restaurant entity."""
    name: str
    hours: dict[str, str]
    phone_number: str
    address: str
    tags: List[str] = []
