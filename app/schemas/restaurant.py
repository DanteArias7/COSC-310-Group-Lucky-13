"""Pydantic schemas for restaurant data models."""

from typing import List
from pydantic import BaseModel, Field
from app.schemas.menu import MenuItem

class Restaurant(BaseModel):
    """Restaurant entity."""
    id: int
    user_id: str
    name: str
    hours: dict[str, str]
    phone_number: str
    address: str
    tags: List[str] = []
    menu: List[MenuItem] = []

class RestaurantCreate(BaseModel):
    """schema to create new restaurant"""
    name: str
    hours: dict[str, str]
    phone_number: str
    address: str
    tags: List[str] = []
    menu: List[MenuItem] = Field(...,min_length = 1)

class UpdateRestaurant(BaseModel):
    """Update restaurant entity."""
    name: str
    hours: dict[str, str]
    phone_number: str
    address: str
    tags: List[str] = []

class RestaurantResult(BaseModel):
    """Searched restaurant entity for browsing"""
    id: int
    name: str
    address: str
    todays_hours: str
    tags: List[str] = []
