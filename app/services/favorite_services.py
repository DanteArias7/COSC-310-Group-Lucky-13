"""Service layer for managing user favorites"""

from typing import Any, Dict, List, Protocol
import uuid
from fastapi import HTTPException
from app.schemas.favorite import Favorite
from app.services.restaurant_services import RestaurantServices

# pylint: disable=too-few-public-methods
class FavoriteServices:
    """Favorite Service Class"""

    def __init__(self,
                 repo: IFavoriteRepo,
                 restaurant_service: RestaurantServices
                 ):
        """Initialize instance with repo object"""
        self.repo = repo
        self.restaurant_service = restaurant_service

    def add_favorite(self, payload: Favorite) -> Dict[str, Any]:
        """
        Adds a favorite menu item

        Args:
            payload (Favorite): The favorite to be added

        Returns:
            Dict[str, Any]: The newly added favorite

        Raises:
            HTTPException: If the item is not found
        """

        favorites = self.repo.load_all_favorites()

        restaurant = self.restaurant_service.fetch_restaurant(payload.restaurant_id)

        for item in restaurant.menu:
            if item.id == payload.menu_item_id:
                break

            raise HTTPException(status_code=404, detail="Menu item not found")

        new_favorite = payload.model_dump()
        new_favorite["id"] = str(uuid.uuid4())

        favorites.append(new_favorite)
        self.repo.save_all_favorites(favorites)

        return new_favorite

    def remove_favorite(self, favorite_id: str , user_id: str) -> None:
        """
        Removes a favorite menu item

        Args:
            favorite_id (str): The ID of the favorite to be removed
            user_id (str): The ID of the user attempting to remove the favorite

        Returns:
            None

        Raises:
            HTTPException: If the favorite is not found
        """

        favorites = self.repo.load_all_favorites()

        for fav in favorites:
            if fav["id"] == favorite_id:
                if fav["user_id"] != user_id:
                    raise HTTPException(status_code=403,
                                        detail="Forbidden: You can only delete your own favorites")

                favorites.remove(fav)
                self.repo.save_all_favorites(favorites)
                return
        raise HTTPException(status_code=404, detail="Favorite not found")


class IFavoriteRepo(Protocol):
    """Favorite Repo Interface"""

    def load_all_favorites(self) -> List[Dict[str, Any]]:
        """Load all favorites"""

    def save_all_favorites(self, favorites: List[Dict[str, Any]]) -> None:
        """Save all favorites"""
