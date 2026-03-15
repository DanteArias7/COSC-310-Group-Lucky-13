"""Pydantic schema for payment data."""

from pydantic import BaseModel

class Payment(BaseModel):
    """Payment request payload."""

    user_id: str
    card_number: str
    cvv: str
    expiration_date: str

class PaymentResult(BaseModel):
    """Payment result response."""
    message: str
