"""Service layer for order business logic."""
from datetime import date, datetime
import random
import string
from typing import Any, Dict, List, Protocol
import time

from fastapi import HTTPException
import pandas
from app.schemas.cart import Cart
from app.schemas.order import Order
from app.schemas.payment import Payment, PaymentResult
from app.schemas.notification import Notification
from app.services.notification_services import send_notification
from app.services.restaurant_services import RestaurantServices

#pylint: disable=too-few-public-methods
class OrderServices():
    """Order Service Class"""
    def __init__(self, repo: IOrderRepo, restaurant_service: RestaurantServices = None):
        """Initialize instance with repo object"""
        self.repo = repo
        self.restaurant_service = restaurant_service

    def get_order_by_id(self, order_id: str) -> Dict[str, Any]:
        """Gets an order by an ID

        Args:
            order_id: ID of the order being requested

        Returns:
            The order as a JSON object
        """
        orders = self.repo.load_all_orders_df()
        orders = orders.set_index("id", drop=False)

        try:
            order = orders.loc[order_id].to_dict()

        except KeyError as exc:
            raise HTTPException(status_code=404,
                                detail=f"Order {order_id} Not Found.") from exc

        return order

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

        for cart_item in cart.cart_items:
            self.restaurant_service.validate_menu_item_is_available(cart.restaurant_id,
                                                                    cart_item.item.id)

        new_order = Order(id=new_id,
                          restaurant_id=cart.restaurant_id,
                          customer_id=cart.user_id,
                          assigned_driver_id="",
                          food_items=items,
                          order_date=todays_date,
                          order_value=cart.total,
                          delivery_time=0.0
                          )

        self.repo.save_order(new_order.model_dump())

        send_notification(
            Notification(
                user_id=cart.user_id,
                message=f"Your order {new_id} has been created successfully"
                )
                )

        return new_order

    def accept_delivery(self, order_id: str, driver_id: str) -> Order:
        """Assigns a delivery driver to an order

        Args:
            order_id: The ID of the order having a driver assigned
            driver_id: The ID of the driver being assigned to
            the order

        Returns:
            The order object with the assigned ID"""
        orders = self.repo.load_all_orders_df()
        orders = orders.set_index("id", drop = False)
        order = self.get_order_by_id(order_id)

        if order["assigned_driver_id"] != '':
            raise HTTPException(status_code=409,
                                detail=f"Order {order_id} already"
                                " assigned.")

        if  order["status"] == "Ready_for_pickup" or \
            order["status"] == "Accepted_by_restaurant" or \
            order["status"] == "Preparing":

            order["assigned_driver_id"] = driver_id

            orders.loc[order_id] = order

            self.repo.update_orders(orders.to_dict(orient="records"))

            return Order(**order)

        raise HTTPException(status_code=409,
                            detail=f"Order {order_id} is {order["status"]}"
                            " and Cannot have driver assigned.")


    def update_order_delivery_status(self, order_id: str, status: str):
        """
        Updates the delivery status of an order.

        Rules:
            Status must be in the OrderStatus Literal class

        Args:
            order_id: The ID of the order being updated.
            status: The status to update the order to

        Returns:
            The Updated order object
        """
        orders = self.repo.load_all_orders_df()
        orders = orders.set_index("id", drop = False)
        available_statuses = ["In_transit",
                            "Complete",
                            "Cancelled"]

        if status not in available_statuses:
            raise HTTPException(status_code=422,
                             detail="Invalid status.")

        order = self.get_order_by_id(order_id)

        if order["status"] == "Ready_for_pickup" or \
            order["status"] == "In_transit":
            order["status"] = status

            orders.loc[order_id] = order

            self.repo.update_orders(orders.to_dict(orient="records"))

            return Order(**order)

        raise HTTPException(status_code=409,
                            detail=f"Order {order_id} Not Ready Yet or Cancelled.")


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

    def get_past_orders_by_restaurant_id(self, restaurant_id: int) -> List[Order]:
        """
        Gets all past orders related to a restaurant.

        Args:
            restaurant_id: The ID of the requested restaurants's orders.

        Returns:
            List of Order objects.
        """
        orders = self.repo.load_all_orders()

        user_orders = []

        for order in orders:
            if order["restaurant_id"] == restaurant_id:
                Order(**order)
                user_orders.append(order)

        return user_orders

    def update_order_restaurant_status(self, order_id: str, status: str):
        """
        Updates the restaurannt status of an order.

        Rules:
            Status must be in the OrderStatus Literal class

        Args:
            order_id: The ID of the order being updated.
            status: The status to update the order to

        Returns:
            The Updated order object
        """
        orders = self.repo.load_all_orders_df()
        orders = orders.set_index("id", drop=False)
        available_statuses = ["Accepted_by_restaurant",
                            "Preparing",
                            "Ready_for_pickup",
                            "Cancelled"]

        if status not in available_statuses:
            raise HTTPException(status_code=422,
                             detail="Invalid status.")

        order = self.get_order_by_id(order_id)

        if order["status"] == "Paid" or \
            order["status"] == "Accepted_by_restaurant" or \
            order["status"] == "Preparing":
            order["status"] = status
            orders.loc[order_id] = order
            self.repo.update_orders(orders)

            return Order(**order)

        raise HTTPException(status_code=409,
                            detail=f"Order {order_id} is {order["status"]}"
                            " and Cannot have status updated.")

    def simulate_payment(self, order_id: str , payment: Payment) -> PaymentResult:
        """
        Simulates the payment process for an order.

        Args:
            order_id: The ID of the order to simulate payment for.
            payment: Payment object containing the payment details to validate.

        Returns:
            The payment result.
        """
        orders = self.repo.load_all_orders()

        for i, order in enumerate(orders):
            if order["id"] == order_id:

                if order["status"] != "Pending":
                    raise HTTPException(status_code=400,
                                        detail=f"Order {order_id} is not in a payable state")

                self.validate_payment_details(payment)

                time.sleep(2)

                orders[i]["status"] = "Paid"
                self.repo.update_orders(orders)

                send_notification(
                    Notification(
                        user_id=order["customer_id"],
                        message=f"Your order {order['id']} has been paid successfully"
                    )
                )

                self.notify_restaurant_owner(order["restaurant_id"], order_id)

                # return payment result
                return PaymentResult(message="Payment Accepted")

        raise HTTPException(status_code=404, detail=f"Order {order_id} Not Found")

    def validate_payment_details(self, payment: Payment) -> bool:
        """
        Validates payment details using predefined rules.

        Args:
        payment: Payment object containing card details.

        Returns:
        True if payment details are valid.

        Raises:
        HTTPException if validation fails.
    """
        card_length = len(payment.card_number)
        if card_length not in [15,16] or not payment.card_number.isdigit():
            raise HTTPException(status_code=400, detail="Payment Rejected: Invalid card number")

        if card_length == 15:
            if len(payment.cvv) != 4 or not payment.cvv.isdigit():
                raise HTTPException(status_code=400, detail="Payment Rejected: Invalid CVV")

        if card_length == 16:
            if len(payment.cvv) != 3 or not payment.cvv.isdigit():
                raise HTTPException(status_code=400, detail="Payment Rejected: Invalid CVV")

        try:
            exp = datetime.strptime(payment.expiration_date, "%m/%y")
            if exp < datetime.now():
                raise HTTPException(status_code=400, detail="Payment Rejected: Card has expired")
        except ValueError as exc:
            raise HTTPException(status_code=400,
                                detail="Payment Rejected: Invalid expiration date") from exc
        return True

    def notify_restaurant_owner(self, restaurant_id: int, order_id: str) -> None:
        """
        Notifies the restaurant owner of a new order.

        Args:
            restaurant_id: The ID of the restaurant to notify.
            order: The Order object containing the order details.

        Returns:
            None
        """
        restaurant = self.restaurant_service.fetch_restaurant(restaurant_id)

        if not restaurant:
            raise HTTPException(status_code=404, detail=f"Restaurant {restaurant_id} Not Found")

        owner_id = restaurant.user_id

        send_notification(
            Notification(
                user_id=owner_id,
                message=f"You have received a new order {order_id}"
            )
        )

    def get_all_available_delivery_orders(self) -> List[Order]:
        """
        Rules:
        - available orders must
            - be Accepted_by_restaurant or Preparing or Ready_for_pickup
            - not have an assigned_driver_id

        Args: none

        Returns:
        A list of Order objects with the matching order status (as specified in rules)
        """
        orders = self.repo.load_all_orders()
        available_orders = []

        for order in orders:
            if ((order["status"] == "Accepted_by_restaurant" or
                order["status"] == "Preparing" or
                order["status"] == "Ready_for_pickup") and
                not order["assigned_driver_id"]):
                available_orders.append(Order(**order))

        return available_orders

    def get_all_pending_paid_orders(self, restaurant_id: str) -> List[Order]:
        """
        Rules:
        - show only pending orders which have been paid successfully
        and with a restaurant_id which matches the requesting user's restaurant,
        so the restaurant may choose to accept or decline

        Args: none

        Returns:
        A list of Order objects with the matching order status (as specified in rules)
        """
        orders = self.repo.load_all_orders()
        pending_paid_orders = []

        for order in orders:
            if order["status"] == "Paid" and order["restaurant_id"] == restaurant_id:
                pending_paid_orders.append(Order(**order))

        return pending_paid_orders

    def get_all_assigned_orders(self, user_id: str) -> List[Order]:
        """
        Rules:
        - order assigned_driver_id should match user_id

        Args:
        user_id: id of delivery driver requesting assigned orders

        Returns:
        A list of Order objects with the matching assigned_driver_id
        """
        orders = self.repo.load_all_orders()
        assigned_orders = []

        for order in orders:
            if order["assigned_driver_id"] == user_id:
                assigned_orders.append(Order(**order))

        return assigned_orders

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
    def load_all_orders_df(self) -> pandas.DataFrame:
        """Loads all orders from csv file

        Returns: All orders in as  List of Dicts."""
    def update_orders(self)-> None:
        """Saves all orders with updates to the data store

        Returns: Nothing """
