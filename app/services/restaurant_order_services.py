# pylint: disable=line-too-long

"""Service layer for restaurant order management."""
from typing import List
from fastapi import HTTPException
from app.schemas.order import Order
from app.services.notification_services import send_notification
from app.schemas.notification import Notification


class RestaurantOrderServices:
    """Handles restaurant owner order management."""

    def __init__(self, order_repo):
        self.order_repo = order_repo

    def get_restaurant_orders(self, restaurant_id: int) -> List[Order]:
        """Get all orders for a restaurant."""
        all_orders = self.order_repo.load_all_orders()
        restaurant_orders = []

        for order_dict in all_orders:
            if order_dict["restaurant_id"] == restaurant_id:
                restaurant_orders.append(Order(**order_dict))

        if not restaurant_orders:
            raise HTTPException(
                status_code=404,
                detail=f"No orders found for restaurant {restaurant_id}"
            )

        return restaurant_orders

    def get_restaurant_order(self, restaurant_id: int, order_id: str) -> Order:
        """Get a specific order for a restaurant."""
        all_orders = self.order_repo.load_all_orders()

        for order_dict in all_orders:
            if order_dict["id"] == order_id:
                if order_dict["restaurant_id"] != restaurant_id:
                    raise HTTPException(
                        status_code=403,
                        detail="Order does not belong to this restaurant"
                    )
                return Order(**order_dict)

        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    def accept_order(self, order_id: str, owner_id: str) -> Order:
        """Restaurant owner accepts an order."""
        # pylint: disable=unused-argument
        orders = self.order_repo.load_all_orders()
        order_dict, index = self._find_order(orders, order_id)

        # Validate order is in correct status
        if order_dict["status"] != "Paid":
            raise HTTPException(
                status_code=422,
                detail=f"Order {order_id} cannot be accepted. "
                       f"Current status: {order_dict['status']}"
            )

        # Update status
        orders[index]["status"] = "Accepted_by_restaurant"
        self.order_repo.update_orders(orders)

        # Notify customer
        send_notification(
            Notification(
                user_id=order_dict["customer_id"],
                message=f"Your order {order_id} has been accepted by the restaurant"
            )
        )

        return Order(**orders[index])

    def update_order_status(self, order_id: str, new_status: str) -> Order:
        """Update order status (Preparing → Ready_for_pickup)."""
        valid_transitions = {
            "Accepted_by_restaurant": ["Preparing"],
            "Preparing": ["Ready_for_pickup"],
            "Ready_for_pickup": []  # Terminal for restaurant actions
        }

        orders = self.order_repo.load_all_orders()
        order_dict, index = self._find_order(orders, order_id)

        # Validate current status allows transition
        if order_dict["status"] not in valid_transitions:
            raise HTTPException(
                status_code=422,
                detail=f"Cannot update status from {order_dict['status']}"
            )

        if new_status not in valid_transitions[order_dict["status"]]:
            raise HTTPException(
                status_code=422,
                detail=f"Cannot transition from {order_dict['status']} to {new_status}"
            )

        # Update status
        orders[index]["status"] = new_status
        self.order_repo.update_orders(orders)

        # Notify appropriate parties
        if new_status == "Ready_for_pickup":
            # Notify drivers that order is ready for pickup
            pass

        return Order(**orders[index])

    def _find_order(self, orders: List[dict], order_id: str):
        """Helper to find order by ID."""
        for i, order in enumerate(orders):
            if order["id"] == order_id:
                return order, i
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
