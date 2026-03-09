"""Service layer for order business logic."""
from datetime import date
import random
import string
from typing import Any, Dict, List, Protocol
import time

from fastapi import HTTPException
from app.schemas.cart import Cart
from app.schemas.order import Order

#pylint: disable=too-few-public-methods
class OrderServices():
    """Order Service Class"""
    def __init__(self, repo: IOrderRepo):
        """Initialize instance with repo object"""
        self.repo = repo


    def place_order(self, cart: Cart) -> Order:
        """
        Places a users order storing it in the order data store and returning
        and order object with the details.

        Args:
            cart: Cart object with all the associated order details, restaurant_id,
            customer id, order date, order value and location.

        Returns:
            New Order Object
        """
        alphanum = string.ascii_letters + string.digits
        new_id = ''.join(random.choice(alphanum) for i in range(7))

        todays_date = date.today().strftime("%m-%d-%Y")
        items = ''

        for item in cart.cart_items:
            items = items + str(item.model_dump()["quantity"]) + "x "
            items = items + str(item.model_dump()["item"]["name"])
            if not item == cart.cart_items[-1]:
                items = items + ', '

        new_order = Order(id=new_id,
                          restaurant_id=cart.restaurant_id,
                          customer_id=cart.user_id,
                          food_items=items,
                          order_date=todays_date,
                          order_value=cart.total,
                          )

        self.repo.save_order(new_order.model_dump())

        return new_order

    def get_orders_by_user_id(self, user_id: str) -> List[Order]:
        """
        Gets all orders related to a user.

        Args:
            user_id: The ID of the requested user's orders.

        Returns:
            List of Order objects.
        """
        orders = self.repo.load_all_orders()

        user_orders = []

        for order in orders:
            if order["customer_id"] == user_id:
                Order(**order)
                user_orders.append(order)

        if not user_orders:
            raise HTTPException(status_code=404,
                                detail="No Orders Found for User")
        return user_orders

    def simulate_payment(self, order_id: str) -> Order:
        """
        Simulates the payment process for an order.

        Args:
            order_id: The ID of the order to simulate payment for.

        Returns:
            The updated Order object with status "Paid".
        """
        orders = self.repo.load_all_orders()

        for i, order in enumerate(orders):
            if order["id"] == order_id:
                # validation check to ensure order is in pending status before simulating payment
                if order["status"] != "Pending":
                    raise HTTPException(status_code=400,
                                        detail=f"Order {order_id} is not in a payable state")

                # simulate payment processing delay
                time.sleep(2)
                orders[i]["status"] = "Paid"
                self.repo.update_orders(orders)
                return Order(**orders[i])

        raise HTTPException(status_code=404, detail=f"Order {order_id} Not Found")


class IOrderRepo(Protocol):
    """Order Repo Interface"""
    def save_order(self, order: Dict[str, Any]) -> None:
        """Saves an order to the data store

        args:
            order: a dict of the order object with all associated
            order attributes

        Returns: Nothing"""
    def load_all_orders(self)-> List[Dict[str, Any]]:
        """Loads all orders from data store

        Returns: A list of dicts representing orders """
