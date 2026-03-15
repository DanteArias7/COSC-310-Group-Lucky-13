"""API Endpoints for Notification functionality"""

from collections.abc import AsyncIterable
from fastapi import APIRouter, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent
from app.schemas.notification import Notification

notification_router = APIRouter(prefix="/notifications",
                                tags=["notification"])

notifications: list[Notification] = []


@notification_router.get("/stream",
                         response_class=EventSourceResponse,
                         status_code=200)
async def stream_notifications(
    user_id: str = Header(..., alias="user-id")) -> AsyncIterable[ServerSentEvent]:
    """Streams notifications to the client using Server-Sent Events (SSE)

    Rules: User must provide a valid user-id header

    Args:
        user_id: header sent with request indicating current user

    Returns:
        Stream of notification events for the user
    """

    for i, notification in enumerate(notifications):

        if notification.user_id == user_id:

            yield ServerSentEvent(
                data=notification,
                event="notification",
                id=str(i)
            )
