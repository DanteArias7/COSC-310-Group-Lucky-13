"""Service layer for cart business logic."""

from typing import Any, Dict, List, Protocol
from fastapi import HTTPException
from app.schemas.cart import Cart
from app.schemas.menu import MenuItem

#pylint: disable=too-few-public-methods
class CartServices():
    """Cart Service Class"""
    def __init__(self, repo: ICartRepo):
        """Initialize instance with repo object"""
        self.repo = repo

    def remove_item_from_cart(self, cart_id: str, menu_item_id: str) -> Cart:
        """Remove a menu item from a user's cart"""
        carts = self.repo.load_all_carts()

        for i, cart in enumerate(carts):
            if cart["id"] == cart_id:
                for menu_item in cart["menu_items"]:
                    if menu_item["id"] == menu_item_id:
                        cart["menu_items"].remove(menu_item)
                        carts[i] = cart
                        self.repo.save_all_carts(carts)
                        return
                raise HTTPException(status_code=404, detail=f"Menu Item {menu_item_id} Not Found")

        raise HTTPException(status_code=404, detail=f"Cart {cart_id} Not Found")

    def add_item_to_cart(self, cart_id: str, restaurant_id: int,payload: MenuItem) -> Cart:
        """Add a menu item to a user's cart"""
        carts = self.repo.load_all_carts()

        for i, cart in enumerate(carts):
            if cart["id"] == cart_id:
                # Ensure all items in cart are from the same restaurant
                if cart["restaurant_id"] != restaurant_id:
                    raise HTTPException(status_code = 400,
                                        detail = "Cannot add items from different " \
                                        "restaurants to the same cart.")
                cart["menu_items"].append(payload.model_dump())
                carts[i] = cart
                self.repo.save_all_carts(carts)
                return Cart(**cart)
        raise HTTPException(status_code=404, detail=f"Cart {cart_id} Not Found")

class ICartRepo(Protocol):
    """User Service Class"""
    def load_all_carts(self) -> List[Dict[str, Any]]:
        """Load all carts"""
    def save_all_carts(self, carts : List[Dict[str , Any]]) -> None:
        """save all carts"""
