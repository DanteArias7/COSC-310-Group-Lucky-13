"""Service layer for restaurant business logic."""

from fastapi import HTTPException
from app.repositories.restaurant_repo import (
    get_all_restaurants,
    get_restaurant_by_id,
)


def fetch_all_restaurants():
    """Return all restaurants."""
    return get_all_restaurants()


def fetch_restaurant(restaurant_id: str):
    """Return a restaurant by ID or raise 404."""
    restaurant = get_restaurant_by_id(restaurant_id)

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found",
        )

    return restaurant
