"""Unit tests for cart methods."""
from fastapi import HTTPException
import pytest
from app.services.cart_services import CartServices
from app.schemas.menu import MenuItem

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
                "total" : 12.99}]

@pytest.fixture
def mocked_repo(mocker):
    """Create mocked repo object for each test"""
    mocked_repo = mocker.Mock()
    return mocked_repo

@pytest.fixture
def mocked_cart_service(mocked_repo):
    """Create service object with mocked repo for each test"""
    return CartServices(mocked_repo)

@pytest.fixture
def menu_item_payload():
    """Sample menu item payload for cart tests"""
    return MenuItem(
        id="018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e02",
        name="Fries",
        description="Crispy golden fries",
        price=5.00,
        tags=["fries"]
    )

@pytest.fixture
def menu_item_payload_second():
    """Second sample menu item payload for cart tests"""
    return MenuItem(
        id="018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e03",
        name="Pizza",
        description="Cheesy pepperoni pizza",
        price=15.00,
        tags=["pizza"]
    )

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

# add_menu_item_to_cart Tests

def test_add_menu_item_to_nonexistent_cart(test_carts, mocked_repo,
                                           mocked_cart_service, menu_item_payload):
    """Test that add_item_to_cart raises exception if cart not found"""

    mocked_repo.load_all_carts.return_value = test_carts

    with pytest.raises(HTTPException) as exc_info:
        mocked_cart_service.add_item_to_cart("fake-id",
                                              menu_item_payload)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Cart fake-id Not Found"

def test_add_menu_item_to_cart(test_carts, mocked_repo,
                               mocked_cart_service, menu_item_payload):
    """Test that add_item_to_cart successfully adds an item"""

    mocked_repo.load_all_carts.return_value = test_carts

    result = mocked_cart_service.add_item_to_cart(
         "00000000-0000-0000-0000-000000000001",
         menu_item_payload
         )
    assert len(result.menu_items) == 2
    assert result.menu_items[1].id == menu_item_payload.id
    mocked_repo.save_all_carts.assert_called_once()

# Test that adding an item from a different restaurant raises an exception
def test_validate_cart_from_different_restaurant(test_carts, mocked_cart_service):
    """Test that validate_cart_from_same_restaurant raises exception when restaurant ids differ"""

    cart = test_carts[0]

    with pytest.raises(HTTPException) as exc_info:
        mocked_cart_service.validate_cart_from_same_restaurant(cart, 102)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Cannot add items from different restaurants to the same cart."

# Test that adding multiple items from same restaurant raises no exception
def test_validate_cart_same_restaurant(test_carts, mocked_cart_service):
    """Test that validation passes when restaurant ids match"""

    cart = test_carts[0]

    mocked_cart_service.validate_cart_from_same_restaurant(cart, 101)
