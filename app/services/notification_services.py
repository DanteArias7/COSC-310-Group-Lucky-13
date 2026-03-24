"""Service for handling notifications."""
import asyncio
from app.schemas.notification import Notification

notifications: dict[str, list[Notification]] = {}

user_queues: dict[str, asyncio.Queue] = {}


def send_notification(notification: Notification):
    """
    Sends a notification to the specified user.

    Args:
        notification: The Notification object containing the user_id and message.

    Returns:
        None
    """

    user_id = notification.user_id

    if user_id not in notifications:
        notifications[user_id] = []

    notifications[user_id].append(notification)


    if user_id in user_queues:
        user_queues[user_id].put_nowait(notification)
