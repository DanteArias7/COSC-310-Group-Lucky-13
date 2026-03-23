"""API Endpoints for Notification functionality"""

import asyncio
from fastapi import APIRouter, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent

from app.services.notification_services import notifications, user_queues

notification_router = APIRouter(prefix="/notifications",
                                tags=["notification"])

@notification_router.get("/stream",
                         response_class=EventSourceResponse,
                         status_code=200)
async def stream_notifications(
    user_id: str = Header(..., alias="user-id")):
    """Streams notifications to the client using Server-Sent Events (SSE)

    Rules: User must provide a valid user-id header

    Args:
        user_id: header sent with request indicating current user

    Returns:
        Stream of notification events for the user
    """

    queue: asyncio.Queue = asyncio.Queue()

    user_queues[user_id] = queue

    for notification in notifications.get(user_id, []):
        yield ServerSentEvent(
                data=notification,
                event="notification"
            )

    try:
        while True:
            notification = await queue.get()
            yield ServerSentEvent(
                data=notification,
                event="notification"
                )

    finally:
        user_queues.pop(user_id, None)
