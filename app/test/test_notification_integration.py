"""Integration tests for the notification streaming endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

@pytest.mark.anyio
async def test_sse_stream_missing_header_returns_422():
    """Tests that the notification stream endpoint returns a
    422 error when the required user-id header is missing."""

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        response = await client.get("/notifications/stream")
    assert response.status_code == 422
