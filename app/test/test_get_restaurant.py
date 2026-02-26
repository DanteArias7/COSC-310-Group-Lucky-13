"""Tests for restaurant functionality."""

from fastapi import HTTPException
import pytest
from app.schemas.menu import CreateMenuItem, MenuItem
from app.services.restaurant_services import RestaurantServices

test_restaurants = [{"id": "00000000-0000-0000-0000-0000000000001", "name": "Veggie Palace",
                "hours": {"Monday": "9:00-17:00"}, "phone_number": "1234567890",
                "address": "123 Green Street",
                "tags": ["vegan", "brunch"],
                "menu": [{"id": "00000000-0000-0000-0000-0000000000001", 
                "name": "Vegan Burger", "description": "Plant-based patty with lettuce and tomato",
                "price": 12.99, "tags": ["vegan"]
                }]
        }]

def test_fetch_all_restaurants(mocker):
    """Testing that fetch_all_restaurants returns a list of restaurants"""
    fake_data = [
        {
            "id": "test-id-123",
            "name": "Veggie Palace",
            "hours": {"Monday": "9:00-17:00"},
            "phone_number": "1234567890",
            "address": "123 Green Street",
            "tags": ["vegan"],
            "menu": []
        }
    ]

    mocked_repo = mocker.Mock()
    restaurant_service = RestaurantServices(mocked_repo)

    mocked_repo.load_all_restaurants.return_value = fake_data

    result = restaurant_service.fetch_all_restaurants()

    assert result == fake_data


def test_fetch_restaurant_success(mocker):
    """Testing that fetch_restaurant returns the result when requested ID exists"""
    fake_restaurant = [{
        "id": "test-id-123",
        "name": "Veggie Palace",
        "hours": {"Monday": "9:00-17:00"},
        "phone_number": "1234567890",
        "address": "123 Green Street",
        "tags": ["vegan"],
        "menu": [] 
    }]

    mocked_repo = mocker.Mock()
    restaurant_service = RestaurantServices(mocked_repo)

    mocked_repo.load_all_restaurants.return_value = fake_restaurant

    result = restaurant_service.fetch_restaurant("test-id-123")
    result = result.model_dump()

    assert result["id"] == "test-id-123"
    assert result["name"] == "Veggie Palace"
    assert result["phone_number"] == "1234567890"
    assert result["address"] == "123 Green Street"
    assert result["hours"]["Monday"] == "9:00-17:00"
    assert result["tags"] == ["vegan"]
    assert result["menu"] == []


def test_fetch_restaurant_not_found(mocker):
    """Testing that fetch_restaurant raises HTTPException when ID does not exist"""

    mocked_repo = mocker.Mock()
    restaurant_service = RestaurantServices(mocked_repo)

    mocked_repo.load_all_restaurants.return_value = []


    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.fetch_restaurant("non-existent-id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Restaurant not found"

def test_add_menu_item(mocker):
    """Test that adding a menu item returns the proper menu item"""
    mocked_uuid = '00000000-0000-0000-0000-000000000002'
    uuid_mock = mocker.patch("app.services.restaurant_services.uuid.uuid7")
    uuid_mock.return_value = mocked_uuid

    mocked_repo = mocker.Mock()
    restaurant_service = RestaurantServices(mocked_repo)

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    payload = CreateMenuItem(name="Classic Burger", description="Cheeseburger",
                             price= 10.50, tags=["burger"])

    expected_menu_item = MenuItem(id=mocked_uuid,name="Classic Burger", description="Cheeseburger",
                                  price= 10.50, tags=["burger"])

    new_menu_item = restaurant_service.add_item_to_menu(test_restaurants[0]["id"], payload)

    assert new_menu_item == expected_menu_item
