"""Restaurant API endpoints"""

from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends
from app.schemas.restaurant import Restaurant
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
    user_service = RestaurantServices(repo)
    return user_service.fetch_all_restaurants()

@restaurant_router.get("/{restaurant_id}", response_model=Restaurant, status_code=200)
def get_restaurant_by_id(restaurant_id: str, repo: RestaurantRepo=Depends(create_restaurant_repo)):
    """Return a specific restaurant by its ID."""
    user_service = RestaurantServices(repo)
    return user_service.fetch_restaurant(restaurant_id)
