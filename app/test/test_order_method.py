"""Tests for restaurant functionality."""
from datetime import date
import pytest
from app.schemas.cart import Cart
from app.services.order_services import OrderServices

#pylint: disable=redefined-outer-name
#pylint: disable=duplicate-code
#pylint: disable=too-few-public-methods
@pytest.fixture
def mocked_repo(mocker):
    """Creates a mocked repo object for each test"""
    return mocker.Mock()

@pytest.fixture
def order_service(mocked_repo):
    """Creates a restaurant service object with mocked repo"""
    return OrderServices(mocked_repo)

@pytest.fixture
def test_carts():
    """Initilize Test cart data for each test"""
    return [{"id" : "00000000-0000-0000-0000-000000000001",
            "user_id" : "00000000-0000-0000-0000-000000000001",
            "restaurant_id" : 101,
            "cart_items" :  [{"item": {"id": "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01",
                            "name": "Vegan Burger",
                            "description": "Plant-based patty with lettuce and tomato",
                            "price": 12.50,
                            "tags": ["vegan"]},
                            "quantity": 2},
                            {"item": {"id": "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01",
                            "name": "Bacon Burger",
                            "description": "Burger with bacon",
                            "price": 10.50,
                            "tags": ["vegan"]},
                            "quantity": 1}],
                "subtotal" : 23.00,
                "tax" : 1.35,
                "total" : 24.35}]


#place_order Unit Tests
def test_place_order_success(mocker, mocked_repo, order_service, test_carts):
    """Scenario: check that creating a valid order returns a valid order object"""
    mocked_random = "Q"
    id_mock = mocker.patch("app.services.order_services.random.choice")
    id_mock.return_value = mocked_random


    class MockedDate():
        """Mocked date class"""
        @classmethod
        def today(cls):
            """Mocked date.today method
            Returns:
                    test date"""
            return date(2026, 3, 6)

    mocked_date = "03-06-2026"
    mocker.patch("app.services.order_services.date", MockedDate)


    mocked_repo.save_order.return_value = None

    cart = Cart(**test_carts[0])

    order = order_service.place_order(cart)

    expected_order = {"id": "QQQQQQQ",
                      "restaurant_id": 101,
                      "customer_id": "00000000-0000-0000-0000-000000000001",
                      "food_items": "2x Vegan Burger, 1x Bacon Burger",
                      "order_date": mocked_date,
                      "order_value": 24.35}

    assert order.model_dump() == expected_order
