"""Integration tests for the notification streaming endpoint."""

import asyncio
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.notification_services import notifications, user_queues, STREAM_STOP


@pytest.mark.anyio
async def test_sse_stream_success():
    """Tests that the notification stream endpoint successfully
    streams notifications to the client."""

    notifications.clear()
    user_queues.clear()

    async def send_stop():
        while "123" not in user_queues:
            await asyncio.sleep(0.01)
        user_queues["123"].put_nowait(STREAM_STOP)

    asyncio.create_task(send_stop())

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        async with client.stream("GET", "/notifications/stream",
                                 headers={"user-id": "123"}) as response:
            assert response.status_code == 200

@pytest.mark.anyio
async def test_sse_stream_missing_header_returns_422():
    """Tests that the notification stream endpoint returns a
    422 error when the required user-id header is missing."""

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        response = await client.get("/notifications/stream")
    assert response.status_code == 422
