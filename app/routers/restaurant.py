"""Router layer for restaurant endpoints."""

from fastapi import APIRouter
from app.services.restaurant_services import (
    fetch_all_restaurants,
    fetch_restaurant,
)

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"],
)


@router.get("/")
def get_all_restaurants():
    """Return a list of all restaurants."""
    return fetch_all_restaurants()


@router.get("/{restaurant_id}")
def get_restaurant_by_id(restaurant_id: str):
    """Return a specific restaurant by its ID."""
    return fetch_restaurant(restaurant_id)
