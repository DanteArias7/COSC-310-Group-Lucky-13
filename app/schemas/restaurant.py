"""Pydantic schemas for restaurant data models."""

from typing import List
from pydantic import BaseModel, Field
from app.schemas.menu import CreateMenuItem, MenuItem
from app.schemas.rating import Rating

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
    average_rating: float | None
    ratings: List[Rating]

class RestaurantCreate(BaseModel):
    """schema to create new restaurant"""
    name: str
    hours: dict[str, str]
    phone_number: str
    address: str
    tags: List[str] = []
    menu: List[CreateMenuItem] = Field(...,min_length = 1)

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
    average_rating: float | None
