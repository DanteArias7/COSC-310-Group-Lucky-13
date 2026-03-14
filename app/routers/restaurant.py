"""Restaurant API endpoints"""

from pathlib import Path
import sys
from typing import List
import random
from fastapi import APIRouter, Depends, Header, Query, status
from app.repositories.cart_repo import CartRepo
from app.repositories.user_repo import UserRepo
from app.schemas.menu import CreateMenuItem, MenuItem, UpdateMenuItem
from app.schemas.restaurant import Restaurant, UpdateRestaurant, RestaurantCreate, RestaurantResult
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
    """Initalize repo object with data path to user json file"""
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
    return restaurant_service.create_new_restaurant(user_id, payload)

@restaurant_router.get("/browse", response_model=List[RestaurantResult], status_code=200)
def browse_restaurants(restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str = Header(...,alias="user-id"),
                        search: str | None = None,
                        tags: List[str] | None = Query(None)):
    """API endpoint for a user to browse all the restaurants
        Args:
            user_id: The id of the user viewing the restaurants,
            restaurant_repo: Restaurant Repo object to access the restaurant data store
            user_repo: User Repo object to allow the authorization
            service object to access user data store,
            search: string to be compared to restaurant names,
            tags: List of strings representing restaurant tags

        Returns:
            If search is None:
                A List of RestaurantResult objects for all restaurants,
                that includes a restaurants id, name, address,
                day's hours, and tags

            If search is str:
                The List of RestaurantResult objects will contain
                restaurants who's name contains the search string.

            If tags is List[str]:
                The List of RestaurantResult objects will contain
                restaurants who's tags include all tags in the tags argument.
        """
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "browse_restaurants")
    if search is None and tags is None:
        return restaurant_service.fetch_all_restaurants()

    if tags is None:
        return restaurant_service.fetch_name_searched_restaurants(search)

    if search is None:
        restaurants = restaurant_service.fetch_all_restaurants()
        return restaurant_service.filter_restaurants_by_tags(restaurants, tags)

    searched_restaurants = restaurant_service.fetch_name_searched_restaurants(search)
    return restaurant_service.filter_restaurants_by_tags(searched_restaurants, tags)

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
    authorization_service.authorize_access(user_id,
                            restaurant_service.fetch_restaurant(restaurant_id).user_id)
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
    authorization_service.authorize_access(user_id,
                            restaurant_service.fetch_restaurant(restaurant_id).user_id)
    return restaurant_service.delete_restaurant(restaurant_id)

@restaurant_router.get("/{restaurant_id}/menu", response_model=List[MenuItem], status_code=200)
def browse_menu_items(restaurant_id: int,
                        restaurant_repo: RestaurantRepo=Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id"),
                        search: str | None = None,
                        price_max: float = sys.float_info.max,
                        price_min: float = 0.00):
    """API endpoint for a user to browse a given restaurants menu
    Args:
        user_id: The id of the user viewing the restaurants,
        restaurant_id: The ID of the restaurant whose menu is being browsed
        restaurant_repo: Restaurant Repo object to access the restaurant data store
        user_repo: User Repo object to allow authorization service object to access user data store,
        search: An optional argument, a string to compare the menu items names to, None by default
        max: An optional argument, the max of the given price range. Max float by default
        min: AN optional argument, the min of the given price range. 0.00 by default

    Returns:
        A List of MenuItem objects, whose names include the search string and/or
        are within the price range.
    """
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "browse_restaurants")

    restaurant = restaurant_service.fetch_restaurant(restaurant_id)
    menu_items = restaurant.menu

    if search is not None:
        menu_items = restaurant_service.get_name_searched_menu_items(restaurant, search)

    if(price_max != sys.float_info.max or price_min != 0.00):
        return restaurant_service.filter_menu_items_by_price(menu_items, price_max, price_min)

    return menu_items


@restaurant_router.post("/{restaurant_id}/menu", response_model=MenuItem, status_code=201)
def add_menu_item_to_menu(restaurant_id: int, payload: CreateMenuItem,
                        restaurant_repo: RestaurantRepo=Depends(create_restaurant_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id")):
    """Add a menu item to the specifed restaurants menu"""
    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_menu")
    authorization_service.authorize_access(user_id,
                                restaurant_service.fetch_restaurant(restaurant_id).user_id)
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
    authorization_service.authorize_access(user_id,
                                restaurant_service.fetch_restaurant(restaurant_id).user_id)
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
    authorization_service.authorize_access(user_id,
                                    restaurant_service.fetch_restaurant(restaurant_id).user_id)
    return restaurant_service.delete_menu_item(restaurant_id, menu_item_id)

@restaurant_router.post("/{restaurant_id}/cart", status_code=201)
def add_user_cart_for_a_resataurant(restaurant_id: int,
                        cart_repo: CartRepo=Depends(create_cart_repo),
                        user_repo: UserRepo = Depends(create_user_repo),
                        user_id: str  = Header(...,alias="user-id")):
    """API endpoint for a user to start a cart associated with a specific restauranat
        Args:
        user_id: The id of the user creating the cart,
        restaurant_id: The id of the restaurant the cart belongs,
        cart_repo: Cart Repo object to allow cart service object to access cart data store,
        user_repo: User Repo object to allow authorization service object to access user data store,
        Returns:
        A Cart object containing the user and restaurant id with no items and a total price of 0.00.
        """
    cart_service = CartServices(cart_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_cart")
    return cart_service.start_cart(user_id, restaurant_id, )

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
    authorization_service.authorize_access(user_id, cart_service.fetch_cart(cart_id).user_id)
    updated_cart = cart_service.remove_item_from_cart(cart_id, menu_item_id)
    temp_dist = random.uniform(1.00, 20.00)
    return cart_service.calculate_cart(updated_cart, temp_dist)

@restaurant_router.post("/{restaurant_id}/cart/{cart_id}",
                        status_code=status.HTTP_201_CREATED)
def add_menu_item_to_cart(cart_id: str,
                          payload: MenuItem,
                          repo: CartRepo = Depends(create_cart_repo),
                          user_repo: UserRepo = Depends(create_user_repo),
                          user_id: str = Header(..., alias="user-id")):
    """Add a menu item to a user's cart"""
    cart_service = CartServices(repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "manage_own_cart")
    authorization_service.authorize_access(user_id, cart_service.fetch_cart(cart_id).user_id)
    updated_cart = cart_service.add_item_to_cart(cart_id, payload)
    temp_dist = random.uniform(1.00, 20.00)
    return cart_service.calculate_cart(updated_cart, temp_dist)
