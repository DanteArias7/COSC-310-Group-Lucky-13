"""Integration tests for restaurant endpoints."""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_all_restaurants_integration():
    """Test retrieving all restaurants via GET /restaurants/."""
    response = client.get("/restaurants/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    restaurant = data[0]

    assert "id" in restaurant
    assert "name" in restaurant
    assert "phone_number" in restaurant
    assert "address" in restaurant
    assert "hours" in restaurant
    assert "tags" in restaurant

    assert isinstance(restaurant["hours"], dict)
    assert isinstance(restaurant["tags"], list)


def test_get_single_restaurant_integration():
    """Test retrieving a single restaurant via GET /restaurants/{id}."""
    response = client.get("/restaurants/00000000-0000-0000-0000-0000000000001")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == "00000000-0000-0000-0000-0000000000001"
    assert "name" in data
    assert "phone_number" in data
    assert "hours" in data
    assert "tags" in data
    assert "address" in data


def test_get_nonexistent_restaurant_integration():
    """Test retrieving a restaurant that does not exist."""
    response = client.get("/restaurants/non-existent-id")

    assert response.status_code == 404
