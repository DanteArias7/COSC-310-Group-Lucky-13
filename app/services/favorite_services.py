"""Service layer for managing user favorites"""

from typing import Any, Dict, List, Protocol

from app.services.restaurant_services import RestaurantServices
from app.services.cart_services import CartServices

# pylint: disable=too-few-public-methods
class FavoriteServices:
    """Favorite Service Class"""

    def __init__(self,
                 repo: IFavoriteRepo,
                 restaurant_service: RestaurantServices,
                 cart_service: CartServices):
        """Initialize instance with repo object"""
        self.repo = repo
        self.restaurant_service = restaurant_service
        self.cart_service = cart_service

class IFavoriteRepo(Protocol):
    """Favorite Repo Interface"""

    def load_all_favorites(self) -> List[Dict[str, Any]]:
        """Load all favorites"""

    def save_all_favorites(self, favorites: List[Dict[str, Any]]) -> None:
        """Save all favorites"""
