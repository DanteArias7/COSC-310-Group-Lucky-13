"""Pydantic schemas for order data models."""
from pydantic import BaseModel

class Order(BaseModel):
    """Order entity."""
    id: str
    restaurant_id: int
    customer_id: str
    food_items: str
    order_date: str
    order_value: float
    status: str = "Pending"
