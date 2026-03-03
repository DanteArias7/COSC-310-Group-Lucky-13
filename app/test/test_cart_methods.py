"""Unit tests for cart methods."""
from fastapi import HTTPException
import pytest
from app.services.cart_services import CartServices

#pylint: disable=redefined-outer-name
@pytest.fixture
def test_carts():
    """Test cart data"""
    return [{"id" : "00000000-0000-0000-0000-000000000001",
            "user_id" : "00000000-0000-0000-0000-000000000001",
            "restaurant_id" : 101,
            "menu_items" :  [{"id": "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01",
                            "name": "Vegan Burger",
                            "description": "Plant-based patty with lettuce and tomato",
                            "price": 12.99,
                            "tags": ["vegan"]}],
                "total" : 7.88}]

@pytest.fixture
def mocked_repo(mocker):
    """Create mocked repo object for each test"""
    mocked_repo = mocker.Mock()
    return mocked_repo

@pytest.fixture
def mocked_cart_service(mocked_repo):
    """Create service object with mocked repo for each test"""
    return CartServices(mocked_repo)

#delete_menu_item_from_cart Tests

def test_delete_menu_item_from_nonexistent_cart(test_carts, mocked_repo, mocked_cart_service):
    """Test that remove_item_from_cart raises an exception if the cart id is not found"""

    mocked_repo.load_all_carts.return_value = test_carts

    with pytest.raises(HTTPException) as exc_info:
        mocked_cart_service.remove_item_from_cart("fake-id",
        "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Cart fake-id Not Found"

def test_delete_nonexistent_menu_item_from_cart(test_carts, mocked_repo, mocked_cart_service):
    """Test that remove_iten_from_cart raises an exception if the menu item id is not found"""

    mocked_repo.load_all_carts.return_value = test_carts

    with pytest.raises(HTTPException) as exc_info:
        mocked_cart_service.remove_item_from_cart("00000000-0000-0000-0000-000000000001",
        "fake-id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Menu Item fake-id Not Found"
