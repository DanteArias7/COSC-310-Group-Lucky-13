"""Service layer for restaurant business logic."""

from typing import Any, Dict, List, Protocol
from fastapi import HTTPException
from app.schemas.restaurant import Restaurant

class RestaurantServices():
    """Restaurant service methods"""
    def __init__(self, repo: IRestaurantRepo):
        """Initialize instance with repo object"""
        self.repo = repo

    def fetch_all_restaurants(self) -> List[Dict[str, Any]]:
        """Return all restaurants."""
        return self.repo.load_all_restaurants()

    def fetch_restaurant(self, restaurant_id: str) -> Restaurant:
        """Return a restaurant by ID or raise 404."""
        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                return Restaurant(**restaurant)

        raise HTTPException(
                status_code=404,
                detail="Restaurant not found",
            )
#pylint: disable=too-few-public-methods
class IRestaurantRepo(Protocol):
    """User Service Class"""
    def load_all_restaurants(self) -> List[Dict[str, Any]]:
        """Load all users"""  
