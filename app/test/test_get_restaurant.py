
"""Tests for restaurant functionality."""

from fastapi import HTTPException
import pytest

from app.services.restaurant_services import fetch_all_restaurants
from app.services.restaurant_services import fetch_restaurant


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
        }
    ]

    mocker.patch(
        "app.services.restaurant_services.get_all_restaurants",
        return_value=fake_data,
    )

    result = fetch_all_restaurants()

    assert result == fake_data


def test_fetch_restaurant_success(mocker):
    """Testing that fetch_restaurant returns the result when requested ID exists"""
    fake_restaurant = {
        "id": "test-id-123",
        "name": "Veggie Palace",
        "hours": {"Monday": "9:00-17:00"},
        "phone_number": "1234567890",
        "address": "123 Green Street",
        "tags": ["vegan"],
    }

    mocker.patch(
        "app.services.restaurant_services.get_restaurant_by_id",
        return_value=fake_restaurant,
    )

    result = fetch_restaurant("test-id-123")

    assert result["id"] == "test-id-123"

def test_fetch_restaurant_not_found(mocker):
    """Testing that fetch_restaurant raises HTTPException when ID does not exist"""

    mocker.patch(
        "app.services.restaurant_services.get_restaurant_by_id",
        return_value=None,
    )

    with pytest.raises(HTTPException) as exc_info:
        fetch_restaurant("non-existent-id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Restaurant not found"