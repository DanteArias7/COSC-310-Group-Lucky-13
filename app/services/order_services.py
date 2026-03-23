"""Service layer for order business logic."""
from datetime import date, datetime
import random
import string
from typing import Any, Dict, List, Protocol
import time

from fastapi import HTTPException
from app.schemas.cart import Cart
from app.schemas.order import Order
from app.schemas.payment import Payment, PaymentResult
from app.schemas.notification import Notification
from app.services.notification_services import send_notification
from app.services.restaurant_services import RestaurantServices

DRIVER_STATUS_TRANSITIONS = {
    "Assigned_to_driver": ["In_transit"],
    "In_transit": ["Complete"]
}

#pylint: disable=too-few-public-methods
class OrderServices():
    """Order Service Class"""
    def __init__(self, repo: IOrderRepo, restaurant_service: RestaurantServices = None): # pylint: disable=used-before-assignment
        """Initialize instance with repo object"""
        self.repo = repo
        self.restaurant_service = restaurant_service

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

    def get_available_orders(self) -> List[Order]:
        """Get all orders ready for pickup with no driver assigned.

        Used by drivers to see available deliveries.
        """
        all_orders = self.repo.load_all_orders()
        available_orders = []

        for order_dict in all_orders:
            # Order must be ready for pickup AND no driver assigned
            if (order_dict["status"] == "Ready_for_pickup" and
                not order_dict["assigned_driver_id"]):
                available_orders.append(Order(**order_dict))

        return available_orders

    def accept_delivery(self, order_id: str, driver_id: str) -> Order:
        """Driver accepts an order to deliver.

        Rules:
        - Order must be in 'Ready_for_pickup' status
        - Order must not have an assigned driver
        - Assigns driver to order, status changes to 'Assigned_to_driver'
        """
        orders = self.repo.load_all_orders()
        order_dict, index = self._find_order(orders, order_id)

        # Validate order is ready for pickup
        if order_dict["status"] != "Ready_for_pickup":
            raise HTTPException(
                status_code=422,
                detail=f"Order {order_id} is not ready for pickup. "
                    f"Current status: {order_dict['status']}"
            )

        # Validate no driver assigned
        if order_dict["assigned_driver_id"]:
            raise HTTPException(
                status_code=409,
                detail=f"Order {order_id} already assigned to driver "
                    f"{order_dict['assigned_driver_id']}"
            )

        # Assign driver and update status
        orders[index]["assigned_driver_id"] = driver_id
        orders[index]["status"] = "Assigned_to_driver"
        self.repo.update_orders(orders)

        # Notify customer
        send_notification(
            Notification(
                user_id=order_dict["customer_id"],
                message=f"Your order {order_id} has been assigned to a driver "
                        "for delivery"
            )
        )

        return Order(**orders[index])

    def _find_order(self, orders: List[Dict[str, Any]], order_id: str):
        """Helper to find order by ID."""
        for i, order in enumerate(orders):
            if order["id"] == order_id:
                return order, i
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    def update_delivery_status(self, order_id: str, driver_id: str,
                           new_status: str) -> Order:
        """Driver updates order delivery status.

        Valid transitions:
        - Assigned_to_driver → In_transit
        - In_transit → Complete

        Customer receives notification on each status update.
        """
        orders = self.repo.load_all_orders()
        order_dict, index = self._find_order(orders, order_id)

        # Validate order assigned to this driver
        if order_dict["assigned_driver_id"] != driver_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update status for orders assigned to you"
            )

        current_status = order_dict["status"]

        # Validate status transition
        if current_status not in DRIVER_STATUS_TRANSITIONS:
            raise HTTPException(
                status_code=422,
                detail=f"Cannot update status from {current_status}"
            )

        if new_status not in DRIVER_STATUS_TRANSITIONS[current_status]:
            raise HTTPException(
                status_code=422,
                detail=f"Cannot transition from {current_status} to {new_status}"
            )

        # Update status
        orders[index]["status"] = new_status
        self.repo.update_orders(orders)

        # Send notification to customer
        message = self._get_delivery_status_message(order_id, new_status)
        send_notification(
            Notification(
                user_id=order_dict["customer_id"],
                message=message
            )
        )

        return Order(**orders[index])

    def _get_delivery_status_message(self, order_id: str, status: str) -> str:
        """Generate user-friendly delivery status update message."""
        messages = {
            "In_transit": f"Your order {order_id} is on its way!",
            "Complete": f"Your order {order_id} has been delivered. "
                        "Thank you for ordering!"
        }
        return messages.get(status, f"Your order {order_id} status: {status}")

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
