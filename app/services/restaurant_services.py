"""Service layer for restaurant business logic."""

from typing import Any, Dict, List, Protocol
import uuid
from fastapi import HTTPException
from app.schemas.menu import MenuItem, UpdateMenuItem
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

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def update_menu_item(self, restaurant_id: str,
                         menu_item_id: str, payload: UpdateMenuItem) -> MenuItem:
        """Add a menu item to a restaurants menu"""

        restaurants = self.repo.load_all_restaurants()

        updated_menu_item = UpdateMenuItem(
                        name=payload.name.strip(),
                        price=payload.price,
                        description=payload.description.strip(),
                        tags=payload.tags
                     )

        for i, restaurant in enumerate(restaurants):
            if restaurant["id"] == restaurant_id:
                for j, menu_item in enumerate(restaurant["menu"]):
                    if menu_item["id"] == menu_item_id:
                        restaurant["menu"][j]={"id" : menu_item_id} | updated_menu_item.model_dump()
                        restaurants[i] = restaurant
                        self.repo.save_all_restaurants(restaurants)
                        return MenuItem(**restaurant["menu"][j])
                raise HTTPException(status_code=404, detail=f"Menu Item {menu_item_id} Not Found")

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

    def delete_menu_item(self, restaurant_id: str, menu_item_id: str) -> None:
        """Deletes user from the data store"""
        restaurants = self.repo.load_all_restaurants()

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                for menu_item in restaurant["menu"]:
                    if menu_item["id"] == menu_item_id:
                        restaurant["menu"].remove(menu_item)
                        self.repo.save_all_restaurants(restaurants)
                        return

                raise HTTPException(status_code=404, detail=f"Menu Item '{menu_item_id}' not found")

        raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

#pylint: disable=too-few-public-methods
class IRestaurantRepo(Protocol):
    """Restaurant reposirtory interface"""
    def load_all_restaurants(self) -> List[Dict[str, Any]]:
        """Load all restaurants"""
    def save_all_restaurants(self, restaurant: List[Dict[str, Any]]):
        """Save all resturants"""
