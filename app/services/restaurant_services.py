"""Service layer for restaurant business logic."""

from typing import Any, Dict, List, Protocol
import uuid
from fastapi import HTTPException
from app.schemas.menu import MenuItem
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

    def add_item_to_menu(self, restaurant_id: str, payload: MenuItem) -> MenuItem:
        """Add a menu item to a restaurants menu"""

        restaurants = self.repo.load_all_restaurants()

        new_id = str(uuid.uuid7())
        new_menu_item = MenuItem(id=new_id,
                        name=payload.name.strip(),
                        price=payload.price,
                        description=payload.description.strip(),
                        tags=payload.tags
                     )
        for i, restaurant in enumerate(restaurants):
            if restaurant["id"] == restaurant_id:
                for menu_item in restaurant["menu"]:
                    if menu_item["name"] == new_menu_item.name:
                        raise HTTPException(status_code=409, detail="Menu Item Already exists")

                restaurant["menu"].append(new_menu_item.model_dump())
                restaurants[i] = restaurant
                self.repo.save_all_restaurants(restaurants)
                return new_menu_item

        raise HTTPException(status_code=404, detail="Restaurant Not Found")

#pylint: disable=too-few-public-methods
class IRestaurantRepo(Protocol):
    """User Service Class"""
    def load_all_restaurants(self) -> List[Dict[str, Any]]:
        """Load all restaurants"""  
    def save_all_restaurants(self, restaurant: List[Dict[str, Any]]):
        """Save all resturants"""
