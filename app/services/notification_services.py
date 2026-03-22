"""Service for handling notifications."""
import asyncio
from app.schemas.notification import Notification

STREAM_STOP  = object()

notifications: dict[str, list[Notification]] = {}

user_queues: dict[str, asyncio.Queue] = {}


def send_notification(notification: Notification):
    """
    Sends notification to user.
    If user is connected, pushes notification to their queue.
    Also stores notification for offline users.
    """

    user_id = notification.user_id

    if user_id not in notifications:
        notifications[user_id] = []

    notifications[user_id].append(notification)


    if user_id in user_queues:
        user_queues[user_id].put_nowait(notification)
