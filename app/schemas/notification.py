"""Pydantic schema for notification models"""
from datetime import datetime
from pydantic import BaseModel

class Notification(BaseModel):
    """Notification entity."""
    user_id: str
    message: str
    timestamp: datetime
