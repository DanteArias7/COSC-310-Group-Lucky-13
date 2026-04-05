"""Integration tests for favorite endpoints."""

import json
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.favorite_repo import FavoriteRepo
from app.repositories.restaurant_repo import RestaurantRepo
from app.repositories.user_repo import UserRepo

from app.routers.favorite_router import (
    create_favorite_repo,
    create_restaurant_repo,
    create_user_repo
)

#pylint: disable=redefined-outer-name

@pytest.fixture
def test_users():
    """Test users"""
    return [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "role": "customer"
        }
    ]

@pytest.fixture
def test_create_favorite_payload():
    """Payload for creating a favorite"""
    return {
        "id": "test-id-1",
        "user_id": "00000000-0000-0000-0000-000000000001",
        "restaurant_id": 101,
        "menu_item_id": "m1"
    }

@pytest.fixture
def test_create_favorite_invalid_menu_item_payload():
    """Payload for creating a favorite with invalid menu item"""
    return {
        "id": "test-id-2",
        "user_id": "00000000-0000-0000-0000-000000000001",
        "restaurant_id": 101,
        "menu_item_id": "invalid"
    }

@pytest.fixture
def test_restaurants():
    """Initialize test restaurant data for test"""
    return [
        {
            "id": 101,
            "user_id": "user1",
            "name": "Test Restaurant",
            "hours": {},
            "phone_number": "123",
            "address": "addr",
            "tags": [],
            "menu": [
                {
                    "id": "m1",
                    "name": "Burger",
                    "description": "desc",
                    "price": 10,
                    "tags": []
                }
            ],
            "average_rating": None,
            "ratings": []
        }
    ]


@pytest.fixture
def temp_favorite_path(tmp_path):
    """Create temporary file for favorites data"""
    path = tmp_path / "favorites.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump([], f)
    return path


@pytest.fixture
def temp_restaurant_path(tmp_path, test_restaurants):
    """Create temporary file for restaurant data"""
    path = tmp_path / "restaurants.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f)
    return path


@pytest.fixture
def temp_user_path(tmp_path, test_users):
    """Create temporary file for user data"""
    path = tmp_path / "users.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(test_users, f)
    return path


@pytest.fixture
def favorite_client(temp_favorite_path, temp_restaurant_path, temp_user_path):
    """Override dependencies"""

    def override_fav():
        return FavoriteRepo(temp_favorite_path)

    def override_rest():
        return RestaurantRepo(temp_restaurant_path)

    def override_user():
        return UserRepo(temp_user_path)

    app.dependency_overrides[create_favorite_repo] = override_fav
    app.dependency_overrides[create_restaurant_repo] = override_rest
    app.dependency_overrides[create_user_repo] = override_user

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_add_favorite_integration(favorite_client , test_create_favorite_payload):
    """
    Spec: Adding a favorite should succeed
    Input: valid restaurant id and menu item id.
    Expected behavior: Favorite is added successfully and returned.
    """
    response = favorite_client.post(
        "/favorites",
        headers={"user-id": "00000000-0000-0000-0000-000000000001"},
        json=test_create_favorite_payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["restaurant_id"] == 101
    assert data["menu_item_id"] == "m1"


def test_add_favorite_invalid_menu_item_integration(favorite_client,
                                                    test_create_favorite_invalid_menu_item_payload):
    """
    Spec: Invalid menu item should return 404
    Input: valid restaurant id and invalid menu item id.
    Expected behavior: HTTPException with status code 404 is raised.
    """
    response = favorite_client.post(
        "/favorites",
        headers={"user-id": "00000000-0000-0000-0000-000000000001"},
        json=test_create_favorite_invalid_menu_item_payload
    )

    assert response.status_code == 404

def test_remove_favorite_integration(favorite_client, test_create_favorite_payload):
    """
    Spec: Removing a favorite should succeed
    Input: valid favorite id.
    Expected behavior: Favorite is removed successfully.
    """

    create_response = favorite_client.post(
        "/favorites",
        headers={"user-id": "00000000-0000-0000-0000-000000000001"},
        json=test_create_favorite_payload
    )

    favorite_id = create_response.json()["id"]

    delete_response = favorite_client.delete(
        f"/favorites/{favorite_id}",
        headers={"user-id": "00000000-0000-0000-0000-000000000001"}
    )
    assert delete_response.status_code == 204

def test_remove_favorite_not_found_integration(favorite_client):
    """
    Spec: Removing a non-existent favorite should return 404
    Input: invalid favorite id.
    Expected behavior: HTTPException with status code 404 is raised.
    """
    delete_response = favorite_client.delete(
        "/favorites/non-existent-id",
        headers={"user-id": "00000000-0000-0000-0000-000000000002"}
    )
    assert delete_response.status_code == 404
