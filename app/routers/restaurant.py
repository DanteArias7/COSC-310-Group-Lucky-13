"""Restaurant API endpoints"""

from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.menu import CreateMenuItem, MenuItem, UpdateMenuItem
from app.schemas.restaurant import Restaurant, UpdateRestaurant
from app.services.restaurant_services import RestaurantServices
from app.repositories.restaurant_repo import RestaurantRepo

RESTAURANT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "restaurants.json"
restaurant_router = APIRouter(
    prefix="/restaurants",
    tags=["restaurant"],
)

def create_restaurant_repo():
    """"Initialize repo object with data path to restaurant json file"""
    return RestaurantRepo(RESTAURANT_DATA_PATH)

@restaurant_router.get("", response_model=List[Restaurant], status_code=200)
def get_all_restaurants(repo: RestaurantRepo = Depends(create_restaurant_repo)):
    """Return a list of all restaurants."""
    restaurant_service = RestaurantServices(repo)
    return restaurant_service.fetch_all_restaurants()

@restaurant_router.get("/{restaurant_id}", response_model=Restaurant, status_code=200)
def get_restaurant_by_id(restaurant_id: str, repo: RestaurantRepo=Depends(create_restaurant_repo)):
    """Return a specific restaurant by its ID."""
    restaurant_service = RestaurantServices(repo)
    return restaurant_service.fetch_restaurant(restaurant_id)

@restaurant_router.put("/{restaurant_id}",
                       response_model=Restaurant, status_code=200)
def update_restaurant(restaurant_id: str, payload: UpdateRestaurant,
                          repo: RestaurantRepo=Depends(create_restaurant_repo)):
    """Update a menu item in a specifed restaurants menu"""
    restaurant_service = RestaurantServices(repo)
    return restaurant_service.update_restaurant(restaurant_id, payload)

@restaurant_router.post("/{restaurant_id}/menu", response_model=MenuItem, status_code=201)
def add_menu_item_to_menu(restaurant_id: str, payload: CreateMenuItem,
                          repo: RestaurantRepo=Depends(create_restaurant_repo)):
    """Add a menu item to the specifed restaurants menu"""
    restaurant_service = RestaurantServices(repo)
    return restaurant_service.add_item_to_menu(restaurant_id, payload)

@restaurant_router.put("/{restaurant_id}/menu/{menu_item_id}",
                       response_model=MenuItem, status_code=200)
def update_menu_item_in_menu(restaurant_id: str, menu_item_id: str, payload: UpdateMenuItem,
                          repo: RestaurantRepo=Depends(create_restaurant_repo)):
    """Update a menu item in a specifed restaurants menu"""
    restaurant_service = RestaurantServices(repo)
    return restaurant_service.update_menu_item(restaurant_id, menu_item_id, payload)

@restaurant_router.delete("/{restaurant_id}/menu/{menu_item_id}",
                          status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item_in_menu(restaurant_id: str, menu_item_id: str,
                          repo: RestaurantRepo=Depends(create_restaurant_repo)):
    """Delete a menu item in a specifed restaurants menu"""
    restaurant_service = RestaurantServices(repo)
    return restaurant_service.delete_menu_item(restaurant_id, menu_item_id)
