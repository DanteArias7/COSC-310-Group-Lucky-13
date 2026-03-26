"""Service layer for cart business logic."""

from typing import Any, Dict, List, Protocol
import uuid
from fastapi import HTTPException
from app.schemas.cart import Cart
from app.schemas.menu import MenuItem

TAX_RATE = 0.10
FEE_PER_KM = 0.35

#pylint: disable=too-few-public-methods
class CartServices():
    """Cart Service Class"""
    def __init__(self, repo: ICartRepo):
        """Initialize instance with repo object"""
        self.repo = repo

    def fetch_cart(self, cart_id: str) -> Cart:
        """Gets a specific cart using its ID
        Args:
        cart_id: The id of the user creating the cart

        Returns:
        A cart object with the matching ID.

        Raises:
        A 404 exception if cart ID does not exist.
        """
        carts = self.repo.load_all_carts()

        for cart in carts:
            if cart["id"]  == cart_id:
                return Cart(**cart)

        raise HTTPException(status_code=404,
                            detail="Cart Not Found.")

    def start_cart(self, user_id: str, restaurant_id: int) -> Cart:
        """Starts a cart associated with a specific user and restauranat
        Args:
        user_id: The id of the user creating the cart
        restaurant_id: The id of the restaurant the cart belongs to
        Returns:
        A Cart object containing the user and restaurant id with no items and a total price of 0.00.
        """
        carts = self.repo.load_all_carts()

        new_id = str(uuid.uuid7())

        new_cart = Cart(id=new_id,
                        user_id=user_id,
                        restaurant_id=restaurant_id)

        carts.append(new_cart.model_dump())
        self.repo.save_all_carts(carts)

        return new_cart

    def calculate_cart(self, cart: Cart, distance : float) -> Cart:
        """Calculate subtotal, delivery fee, tax, and total for a cart.
        Rules:
        - subtotal, delivery fee, tax, and total should be rounded to 2 decimal places
        - delivery fee calculated based on distance * FEE_PER_KM
            (currently only calculated when no delivery fee is set, will be changed in M4)
        - tax calculated based on subtotal * TAX_RATE

        Args:
        - Cart object with up to date CartItems list
            (subtotal, delivery fee, tax, and total not yet updated)
        - distance: float of distance from restaurant to customer
            (distance currently randomly selected, will implement Google API in M4)

        Returns:
            Cart object with updated subtotal, delivery fee tax, and total
        """
        subtotal = round(sum(item.item.price * item.quantity for item in cart.cart_items), 2)
        if cart.delivery_fee == 0:
            delivery_fee = round(distance * FEE_PER_KM, 2)
        else:
            delivery_fee = cart.delivery_fee
        tax = round(subtotal * TAX_RATE, 2)
        total = round(subtotal + delivery_fee + tax, 2)

        return cart.model_copy(update={
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "tax": tax,
            "total": total
        })

    def find_cart_data(self, carts: List[Dict[str, Any]], cart_id: str) -> Dict[str, Any]:
        """Helper method to find cart data by ID, raises 404 if cart doesn't exist."""
        for cart in carts:
            if cart["id"] == cart_id:
                return cart
        raise HTTPException(status_code=404, detail=f"Cart {cart_id} Not Found")

    def remove_item_from_cart(self, cart_id: str, menu_item_id: str) -> Cart:
        """Remove a menu item from a user's cart

        Rules:
        - The cart and menu item must exist.
        - If a multiple instances of the item exists in the cart,
        its quantity should decrease by 1.
        - If only a single instace of the item exists in the cart,
        it should be removed entirely

        Args:
            cart_id: The ID of the cart having an item deleted
            menu_item_id: The ID of the menu item being deleted

        Returns:
            The updated cart object

        Raises:
            A 404 HTTPException if either the menu_item or cart is
            not found"""
        carts = self.repo.load_all_carts()
        cart = self.find_cart_data(carts, cart_id)


        for cart_item in cart["cart_items"]:
            if cart_item["item"]["id"] == menu_item_id:
                if cart_item["quantity"] > 1:
                    cart_item["quantity"] -= 1
                else:
                    cart["cart_items"].remove(cart_item)
                self.repo.save_all_carts(carts)
                return Cart(**cart)
        raise HTTPException(status_code=404, detail=f"Menu Item {menu_item_id} Not Found")

    def add_item_to_cart(self, cart_id: str, payload: MenuItem) -> Cart:
        """
        Adds a menu item to a user's cart.

        Rules:
        - The cart must exist.
        - A cart can only contain items from one restaurant.
        - If the item already exists in the cart, its quantity should increase by 1.
        - If the item does not exist in the cart, it should be added with quantity = 1.
        - After modification, the cart must be saved to persistent storage.

        Args:
        cart_id: The unique identifier of the cart to which the item will be added.
        payload: The MenuItem object representing the item being added.

        Returns:
        Cart: The updated cart object after the item is added or updated.

        Raises:
        HTTPException:
        status_code = 404 if the cart with the given cart_id does not exist.
        """
        carts = self.repo.load_all_carts()
        cart = self.find_cart_data(carts, cart_id)


        self.validate_cart_from_same_restaurant(cart, cart["restaurant_id"])

        for cart_item in cart["cart_items"]:
            if cart_item["item"]["id"] == payload.id:
                cart_item["quantity"] += 1
                break
        else:
            cart["cart_items"].append({"item": payload.model_dump(), "quantity": 1})

        self.repo.save_all_carts(carts)
        return Cart(**cart)

    def validate_cart_from_same_restaurant(self, cart: Dict[str, Any], restaurant_id: int) -> None:
        """
        Validates that all items in a cart belong to the same restaurant.

        Rules:
        - A cart can only contain menu items from one restaurant.
        - If a new item belongs to a different restaurant than the cart's
          existing restaurant_id, the operation must be rejected.

        Args:
        cart: The cart object containing existing cart information.
        restaurant_id: The restaurant ID associated with the menu item being added to the cart.

        Raises:
        HTTPException: status_code = 400 if the restaurant_id does not
        match the cart's restaurant_id.

        Returns:
        None. Validation passes silently if restaurant IDs match.
        """

        if cart["restaurant_id"] != restaurant_id:
            raise HTTPException(status_code = 400,
                                detail = "Cannot add items from different " \
                                "restaurants to the same cart.")

class ICartRepo(Protocol):
    """User Service Class"""
    def load_all_carts(self) -> List[Dict[str, Any]]:
        """Load all carts"""
    def save_all_carts(self, carts : List[Dict[str , Any]]) -> None:
        """save all carts"""
