"""Restaurant API endpoints"""

from typing import List
from fastapi import APIRouter
from app.schemas.restaurant import Restaurant
from app.services.restaurant_services import (
    fetch_all_restaurants,
    fetch_restaurant,
)

restaurant_router = APIRouter(
    prefix="/restaurants",
    tags=["restaurant"],
)


@restaurant_router.get("", response_model=List[Restaurant], status_code=200)
def get_all_restaurants():
    """Return a list of all restaurants."""
    return fetch_all_restaurants()


@restaurant_router.get("/{restaurant_id}", response_model=Restaurant, status_code=200)
def get_restaurant_by_id(restaurant_id: str):
    """Return a specific restaurant by its ID."""
    return fetch_restaurant(restaurant_id)
