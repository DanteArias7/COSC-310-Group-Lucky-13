"""Unit tests for cart methods."""
from fastapi import HTTPException
import pytest
from app.schemas.cart import Cart
from app.services.cart_services import CartServices
from app.schemas.menu import MenuItem

#pylint: disable=redefined-outer-name
@pytest.fixture
def test_carts():
    """Test cart data"""
    return [{"id" : "00000000-0000-0000-0000-000000000001",
            "user_id" : "00000000-0000-0000-0000-000000000001",
            "restaurant_id" : 101,
            "cart_items" :  [{"item": {"id": "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01",
                            "name": "Vegan Burger",
                            "description": "Plant-based patty with lettuce and tomato",
                            "price": 12.99,
                            "tags": ["vegan"]},
                            "quantity": 1}],
                "subtotal" : 0.00,
                "delivery_fee" : 0.00,
                "tax" : 0.00,
                "total" : 0.00}]

@pytest.fixture
def empty_cart():
    """Empty cart with no items"""
    return Cart(**{
        "id": "00000000-0000-0000-0000-000000000002",
        "user_id": "00000000-0000-0000-0000-000000000001",
        "restaurant_id": 101,
        "cart_items": [],
        "subtotal": 0.00, "delivery_fee": 0.00, "tax": 0.00, "total": 0.00
    })

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
def cart_item_payload():
    """Sample menu item payload for cart tests"""
    return MenuItem(
        id="018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e02",
        name="Fries",
        description="Crispy golden fries",
        price=5.00,
        tags=["fries"]
    )

def test_start_cart(mocker, mocked_repo, mocked_cart_service, test_carts):
    """Test that the start cart method returns the proper cart object"""
    mocked_repo.load_all_carts.return_value = test_carts

    mocked_uuid = '00000000-0000-0000-0000-000000000001'
    uuid_mock = mocker.patch("app.services.restaurant_services.uuid.uuid7")
    uuid_mock.return_value = mocked_uuid

    new_cart = mocked_cart_service.start_cart(user_id="00000000-0000-0000-0000-000000000001",
                                   restaurant_id=101)

    test_carts[0]["cart_items"] = []
    test_carts[0]["tax"] = 0.00
    test_carts[0]["subtotal"] = 0.00
    test_carts[0]["total"] = 0.00

    assert new_cart.model_dump() == test_carts[0]
#delete_cart_item_from_cart Tests

def test_delete_cart_item_from_nonexistent_cart(test_carts, mocked_repo, mocked_cart_service):
    """Test that remove_item_from_cart raises an exception if the cart id is not found"""

    mocked_repo.load_all_carts.return_value = test_carts

    with pytest.raises(HTTPException) as exc_info:
        mocked_cart_service.remove_item_from_cart("fake-id",
        "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Cart fake-id Not Found"

def test_delete_nonexistent_cart_item_from_cart(test_carts, mocked_repo, mocked_cart_service):
    """Test that remove_iten_from_cart raises an exception if the menu item id is not found"""

    mocked_repo.load_all_carts.return_value = test_carts

    with pytest.raises(HTTPException) as exc_info:
        mocked_cart_service.remove_item_from_cart("00000000-0000-0000-0000-000000000001",
        "fake-id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Menu Item fake-id Not Found"

# add_cart_item_to_cart Tests

def test_add_cart_item_to_nonexistent_cart(test_carts, mocked_repo, mocked_cart_service,
                                           cart_item_payload):
    """
    Spec: User should not be able to add items to a cart that does not exist.
    Input: cart_id that is not present in repository.
    Expected behavior: System raises HTTPException with status 404.
    """

    mocked_repo.load_all_carts.return_value = test_carts

    with pytest.raises(HTTPException) as exc_info:
        mocked_cart_service.add_item_to_cart("fake-id", cart_item_payload)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Cart fake-id Not Found"

def test_add_cart_item_to_cart(test_carts, mocked_repo, mocked_cart_service, cart_item_payload):
    """
    Spec: If the cart exists, the item should be added to the cart.
    Input: valid cart_id and menu item payload.
    Expected behavior: item is appended to cart_items list.
    """
    mocked_repo.load_all_carts.return_value = test_carts

    result = mocked_cart_service.add_item_to_cart(
         "00000000-0000-0000-0000-000000000001",
         cart_item_payload
         )
    assert len(result.cart_items) == 2
    assert result.cart_items[1].item.id == cart_item_payload.id
    mocked_repo.save_all_carts.assert_called_once()

# Test that adding an item from a different restaurant raises an exception
def test_validate_cart_from_different_restaurant(test_carts, mocked_cart_service):
    """
    Spec: Cart must only contain items from one restaurant.
    Input: cart.restaurant_id = 101, new item restaurant_id = 102.
    Expected behavior: system rejects the operation with HTTP 400.
    """
    cart = test_carts[0]

    with pytest.raises(HTTPException) as exc_info:
        mocked_cart_service.validate_cart_from_same_restaurant(cart, 102)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Cannot add items from different restaurants to the same cart."

# Test that adding multiple items from same restaurant raises no exception
def test_validate_cart_same_restaurant(test_carts, mocked_cart_service):
    """
    Spec: Items from the same restaurant are allowed in the cart.
    Input: cart.restaurant_id = 101, new item restaurant_id = 101.
    Expected behavior: validation passes with no exception.
    """
    cart = test_carts[0]

    mocked_cart_service.validate_cart_from_same_restaurant(cart, 101)

# calculate_cart Tests

def test_calculate_cart(test_carts, mocked_cart_service):
    """Test calculate_cart returns correct totals when distance is 1.0 km."""
    cart = Cart(**test_carts[0])
    result = mocked_cart_service.calculate_cart(cart, 1.0)

    assert result.subtotal     == 12.99
    assert result.delivery_fee == 0.35
    assert result.tax          == 1.30
    assert result.total        == 14.64

def test_calculate_cart_empty_items(mocked_cart_service, empty_cart):
    """Test calculate_cart returns correct totals when cart is empty"""
    result = mocked_cart_service.calculate_cart(empty_cart, 1.0)

    assert result.subtotal     == 0.00
    assert result.delivery_fee == 0.00
    assert result.tax          == 0.00
    assert result.total        == 0.00
