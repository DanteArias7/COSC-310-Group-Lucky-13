"""Restaurant API endpoints"""

from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, Header, status
from app.repositories.cart_repo import CartRepo
from app.repositories.user_repo import UserRepo
from app.schemas.menu import CreateMenuItem, MenuItem, UpdateMenuItem
from app.schemas.restaurant import Restaurant, UpdateRestaurant, RestaurantCreate
from app.services.authorization_services import AuthorizationServices
from app.services.cart_services import CartServices
from app.services.restaurant_services import RestaurantServices
from app.repositories.restaurant_repo import RestaurantRepo
from app.routers.user import USER_DATA_PATH

RESTAURANT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "restaurants.json"
CART_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "carts.json"
restaurant_router = APIRouter(
    prefix="/restaurants",
    tags=["restaurant"],
)

# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
def create_restaurant_repo():
    """"Initialize repo object with data path to restaurant json file"""
    return RestaurantRepo(RESTAURANT_DATA_PATH)

def create_cart_repo():
    """"Initialize repo object with data path to restaurant json file"""
    return CartRepo(CART_DATA_PATH)
def create_user_repo():
    """Initalize repo object with data paht to user json file"""
    return UserRepo(USER_DATA_PATH)

@restaurant_router.post("", response_model=Restaurant, status_code=201)
def create_restaurant(payload: RestaurantCreate,
                      restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
                      user_repo: UserRepo = Depends(create_user_repo),
                      user_id: str = Header(..., alias="user-id")):
    """Create a new restaurant profile."""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_restaurant")
    return restaurant_service.create_new_restaurant(payload)

@restaurant_router.get("", response_model=List[Restaurant], status_code=200)
def get_all_restaurants(restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str = Header(...,alias="user-id")):
    """Return a list of all restaurants."""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "browse_restaurants")
    return restaurant_service.fetch_all_restaurants()

@restaurant_router.get("/{restaurant_id}", response_model=Restaurant, status_code=200)
def get_restaurant_by_id(restaurant_id: int,
                        restaurant_repo: RestaurantRepo=Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id")):
    """Return a specific restaurant by its ID."""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "browse_restaurants")
    return restaurant_service.fetch_restaurant(restaurant_id)

@restaurant_router.put("/{restaurant_id}",
                       response_model=Restaurant, status_code=200)
def update_restaurant(restaurant_id: int, payload: UpdateRestaurant,
                        restaurant_repo: RestaurantRepo=Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id")):
    """Update a restaurant's information'"""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_restaurant")
    return restaurant_service.update_restaurant(restaurant_id, payload)

@restaurant_router.delete("/{restaurant_id}",
                       status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int,
                        restaurant_repo: RestaurantRepo=Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id")):
    """Delete a restaurant listing from the system"""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_restaurant")
    return restaurant_service.delete_restaurant(restaurant_id)

@restaurant_router.post("/{restaurant_id}/menu", response_model=MenuItem, status_code=201)
def add_menu_item_to_menu(restaurant_id: int, payload: CreateMenuItem,
                        restaurant_repo: RestaurantRepo=Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id")):
    """Add a menu item to the specifed restaurants menu"""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_menu")
    return restaurant_service.add_item_to_menu(restaurant_id, payload)

@restaurant_router.put("/{restaurant_id}/menu/{menu_item_id}",
                       response_model=MenuItem, status_code=200)
def update_menu_item_in_menu(restaurant_id: int, menu_item_id: str, payload: UpdateMenuItem,
                        restaurant_repo: RestaurantRepo=Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id")):
    """Update a menu item in a specifed restaurants menu"""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_menu")
    return restaurant_service.update_menu_item(restaurant_id, menu_item_id, payload)

@restaurant_router.delete("/{restaurant_id}/menu/{menu_item_id}",
                          status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item_in_menu(restaurant_id: int, menu_item_id: str,
                        restaurant_repo: RestaurantRepo=Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id")):
    """Delete a menu item in a specifed restaurants menu"""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_menu")
    return restaurant_service.delete_menu_item(restaurant_id, menu_item_id)

@restaurant_router.delete("/{restaurant_id}/cart/{cart_id}/" \
                        "{menu_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item_from_cart(cart_id: str, menu_item_id: str,
                        restaurant_repo: CartRepo=Depends(create_cart_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(..., alias="user-id")):
    """Delate a menu item from a users cart"""
    cart_service = CartServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_cart")
    return cart_service.remove_item_from_cart(cart_id, menu_item_id)
