"""Pydantic schemas for order data models."""
from typing import Literal
from pydantic import BaseModel

OrderStatus = Literal[
    "Pending",
    "Paid",
    "Accepted_by_restaurant",
    "Preparing",
    "Ready_for_pickup",
    "Assigned_to_driver",
    "In_transit",
    "Complete",
    "Cancelled",
]

class Order(BaseModel):
    """Order entity."""
    id: str
    restaurant_id: int
    customer_id: str
    assigned_driver_id: str = ""
    food_items: str
    order_date: str
    order_value: float
    status: OrderStatus = "Pending"
    delivery_time: float = 0.0
