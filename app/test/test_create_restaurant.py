"""Unit and integration tests for create restaurant functionality."""

import json
from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from app.main import app
from app.schemas.restaurant import RestaurantCreate
from app.repositories.restaurant_repo import RestaurantRepo
from app.routers.restaurant import create_restaurant_repo
from app.services.restaurant_services import RestaurantServices

client = TestClient(app)

def test_create_new_restaurant(mocker):
    """Scenario: check that creating a valid restaurant returns a valid restaurant"""
    mocked_uuid = "00000000-0000-0000-0000-000000000099"
    uuid_mock = mocker.patch("app.services.restaurant_services.uuid.uuid4")
    uuid_mock.return_value = mocked_uuid

    mocked_repo = mocker.Mock()
    mocked_repo.load_all_restaurants.return_value = []

    restaurant_service = RestaurantServices(mocked_repo)

    payload = RestaurantCreate(
        name="Taco Town",
        hours={"Monday": "10:00-20:00"},
        phone_number="5555555555",
        address="123 Taco Lane",
        tags=["mexican"],
        menu=[]
    )

    result = restaurant_service.create_new_restaurant(payload)

    assert result.id == mocked_uuid
    assert result.name == "Taco Town"
    assert result.hours == {"Monday": "10:00-20:00"}
    assert result.phone_number == "5555555555"
    assert result.address == "123 Taco Lane"
    assert result.tags == ["mexican"]
    mocked_repo.save_all_restaurants.assert_called_once()

def test_create_restaurant_integration(tmp_path):
    """Test creating a restaurant via POST /restaurants"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_create_restaurant_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_create_restaurant_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump([], f)

    payload = {
        "name": "Taco Town",
        "hours": {"Monday": "10:00-20:00"},
        "phone_number": "5555555555",
        "address": "123 Taco Lane",
        "tags": ["mexican"],
        "menu": []
    }

    r = client.post("/restaurants", json=payload)

    assert r.status_code == 201

    data = r.json()
    assert data["name"] == "Taco Town"
    assert data["hours"] == {"Monday": "10:00-20:00"}
    assert data["phone_number"] == "5555555555"
    assert data["address"] == "123 Taco Lane"
    assert data["tags"] == ["mexican"]
    assert "id" in data

    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert len(restaurants) == 1
    assert restaurants[0]["name"] == "Taco Town"