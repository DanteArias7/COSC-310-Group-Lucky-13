"""Unit tests for the notification streaming endpoint."""

import asyncio
import pytest

from app.services.notification_services import user_queues, send_notification
from app.schemas.notification import Notification

@pytest.mark.anyio
async def test_send_notification_reaches_queue():
    """Test that sending a notification puts it in the user's queue."""
    user_queues["test-user"] = asyncio.Queue()

    send_notification(Notification(user_id="test-user", message="hello"))

    item = user_queues["test-user"].get_nowait()
    assert item.message == "hello"
