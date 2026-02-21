"""Pydantic schemas for restaurant data models."""

from typing import List
from pydantic import BaseModel


class Restaurant(BaseModel):
    """Restaurant entity."""
    id: str
    name: str
    hours: dict[str, str]
    phone_number: str
    address: str
    tags: List[str] = []
