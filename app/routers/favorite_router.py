"""API Endpoints for favorite functionality"""
from pathlib import Path
from fastapi import APIRouter, Depends, Header

from app.schemas.favorite import Favorite

from app.repositories.favorite_repo import FavoriteRepo
from app.repositories.restaurant_repo import RestaurantRepo
from app.repositories.user_repo import UserRepo

from app.services.favorite_services import FavoriteServices
from app.services.authorization_services import AuthorizationServices
from app.services.restaurant_services import RestaurantServices

from app.routers.user import USER_DATA_PATH

FAVORITE_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "favorites.json"
RESTAURANT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "restaurants.json"

favorite_router = APIRouter(
    prefix="/favorites",
    tags=["favorites"]
)

def create_favorite_repo():
    """ Initializes the FavoriteRepo with the path to the favorites data file.
    Returns:
        FavoriteRepo: An instance of the FavoriteRepo class.
    """
    return FavoriteRepo(FAVORITE_DATA_PATH)

def create_restaurant_repo():
    """ Initializes the RestaurantRepo with the path to the restaurants data file.
    Returns:
        RestaurantRepo: An instance of the RestaurantRepo class.
    """
    return RestaurantRepo(RESTAURANT_DATA_PATH)

def create_user_repo():
    """Initalize repo object with data path to user json file
    Returns:
        UserRepo: An instance of the UserRepo class.
    """
    return UserRepo(USER_DATA_PATH)

@favorite_router.post("", status_code=201)
def add_favorite(
    payload: Favorite,
    favorite_repo: FavoriteRepo = Depends(create_favorite_repo),
    restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Add a menu item to favorites"""

    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "browse_restaurants")
    authorization_service.authorize_access(user_id, payload.user_id)

    service = FavoriteServices(
        favorite_repo,
        RestaurantServices(restaurant_repo)
    )

    return service.add_favorite(payload)

@favorite_router.delete("/{favorite_id}", status_code=204)
def remove_favorite(
    favorite_id: str,
    favorite_repo: FavoriteRepo = Depends(create_favorite_repo),
    restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Remove a menu item from favorites"""

    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "browse_restaurants")

    service = FavoriteServices(
        favorite_repo,
        restaurant_service
    )

    service.remove_favorite(favorite_id, user_id)

@favorite_router.get("", status_code=200)
def get_favorites(
    favorite_repo: FavoriteRepo = Depends(create_favorite_repo),
    restaurant_repo: RestaurantRepo = Depends(create_restaurant_repo),
    user_repo: UserRepo = Depends(create_user_repo),
    user_id: str = Header(..., alias="user-id")
):
    """Get all favorites for a user"""

    restaurant_service = RestaurantServices(restaurant_repo)
    authorization_service = AuthorizationServices(user_repo)
    authorization_service.authorize(user_id, "browse_restaurants")

    service = FavoriteServices(
        favorite_repo,
        restaurant_service
    )

    return service.get_favorites_by_user_id(user_id)
