"""Integration tests for the notification streaming endpoint."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

@pytest.mark.anyio
async def test_sse_stream_missing_header_returns_422():
    """
    Spec: If the user-id header is missing, the endpoint should return a 422 error.
    Input: GET request to /notifications/stream without user-id header
    Expected behavior: The response should have a 422 status code.
    """

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        response = await client.get("/notifications/stream")
    assert response.status_code == 422
