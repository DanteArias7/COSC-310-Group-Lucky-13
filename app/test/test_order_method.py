"""Tests for restaurant functionality."""
from datetime import date
from fastapi import HTTPException
import pytest
from app.schemas.cart import Cart
from app.schemas.payment import Payment
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

@pytest.fixture
def test_orders():
    """Initialize test order data for each test"""
    return[{"id": "QQQQQQQ",
                      "restaurant_id": 101,
                      "customer_id": "00000000-0000-0000-0000-000000000001",
                      "assigned_driver_id": "",
                      "food_items": "2x Vegan Burger, 1x Bacon Burger",
                      "order_date": "03-06-2025",
                      "order_value": 24.35,
                      "status": "Pending",
                      "delivery_time": 0.0},
                      {"id": "QQQQQQQ",
                      "restaurant_id": 101,
                      "customer_id": "00000000-0000-0000-0000-000000000001",
                      "assigned_driver_id": "",
                      "food_items": "2x Vegan Burger",
                      "order_date": "03-06-2025",
                      "order_value": 24.35,
                      "status": "Pending",
                      "delivery_time": 0.0},
                      {"id": "QQQQQQQ",
                      "restaurant_id": 101,
                      "customer_id": "00000000-0000-0000-0000-000000000002",
                      "assigned_driver_id": "",
                      "food_items": "1x Hot Dog",
                      "order_date": "03-06-2025",
                      "order_value": 24.35,
                      "status": "Pending",
                      "delivery_time": 0.0}
                      ]

@pytest.fixture
def test_order_status():
    """Initialize test order data with status for payment tests"""
    return[{"id": "AAAAAAA",
         "restaurant_id": 101,
         "customer_id": "00000000-0000-0000-0000-000000000001",
         "food_items": "1x Burger",
         "order_date": "03-06-2026",
         "order_value": 12.50,
         "status": "Pending"}]

@pytest.fixture
def test_order_status_2():
    """Initialize test order data with status for payment tests"""
    return[{"id": "BBBBBBB",
         "restaurant_id": 101,
         "customer_id": "00000000-0000-0000-0000-000000000001",
         "food_items": "1x Burger",
         "order_date": "03-06-2026",
         "order_value": 12.50,
         "status": "Paid"}]

@pytest.fixture
def valid_payment():
    """Valid payment payload"""
    return {
        "user_id" : "00000000-0000-0000-0000-000000000001",
        "card_number": "1234567812345678",
        "cvv": "123",
        "expiration_date": "12/30"
    }

@pytest.fixture
def invalid_card_payment():
    """Invalid card number payment payload"""
    return {
        "user_id" : "00000000-0000-0000-0000-000000000001",
        "card_number": "123",
        "cvv": "123",
        "expiration_date": "12/30"
    }

@pytest.fixture
def invalid_cvv_payment():
    """Invalid CVV payment payload"""
    return {
        "user_id" : "00000000-0000-0000-0000-000000000001",
        "card_number": "1234567812345678",
        "cvv": "12",
        "expiration_date": "12/30"
    }

@pytest.fixture
def expired_payment():
    """Expired card"""
    return {
        "user_id" : "00000000-0000-0000-0000-000000000001",
        "card_number": "1234567812345678",
        "cvv": "123",
        "expiration_date": "01/20"
    }


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
                      "assigned_driver_id": "",
                      "food_items": "2x Vegan Burger, 1x Bacon Burger",
                      "order_date": mocked_date,
                      "order_value": 24.35,
                      "status": "Pending",
                      "delivery_time": 0.0}

    assert order.model_dump() == expected_order

#get_order_by_user_id Unit Tests
def test_get_order_by_user_id_success(mocked_repo, order_service, test_orders):
    """
    Spec: Method should return orders for a user
    Input: valid user_id
    Expected behavior: Method returns List of order objects
    """
    mocked_repo.load_all_orders.return_value = test_orders

    orders = order_service.get_orders_by_user_id(test_orders[0]["customer_id"])

    expected_orders = [test_orders[0], test_orders[1]]

    assert orders == expected_orders

def test_get_order_by_user_id_user_with_no_orders(mocked_repo, order_service, test_orders):
    """
    Spec: Method should return orders for a user
    Input: valid user_id
    Expected behavior: Method returns List of order objects
    """
    mocked_repo.load_all_orders.return_value = test_orders

    with pytest.raises(HTTPException) as exc_info:
        order_service.get_orders_by_user_id("user-with-no-orders")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No Orders Found for User"

#simulate_payment Unit Tests
def test_simulate_payment_success(mocked_repo, order_service, test_order_status, valid_payment):
    """
    Spec: Method should simulate payment for an order
    Input: valid order_id and valid payment details
    Expected behavior: Order status should update to Paid &&
                        method should return payment result message
    """

    mocked_repo.load_all_orders.return_value = test_order_status
    mocked_repo.update_orders.return_value = None

    payment = Payment(**valid_payment)

    result = order_service.simulate_payment(
        test_order_status[0]["id"],
        payment
    )

    assert result.message == "Payment Accepted"
    assert test_order_status[0]["status"] == "Paid"
    mocked_repo.update_orders.assert_called_once()

def test_simulate_payment_order_not_found(mocked_repo, order_service , valid_payment):
    """
    Spec: Method should raise exception if order does not exist
    Input: invalid order_id, valid payment details
    Expected behavior: HTTPException with status 404
    """

    mocked_repo.load_all_orders.return_value = []

    payment = Payment(**valid_payment)

    with pytest.raises(HTTPException) as exc_info:
        order_service.simulate_payment("invalid-id", payment)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Order invalid-id Not Found"

def test_simulate_payment_order_already_paid(mocked_repo, order_service,
                                             test_order_status_2 , valid_payment):
    """
    Spec: Method should raise exception if order is not in pending status
    Input: order_id for order that is not in Pending status, valid payment details
    Expected behavior: HTTPException with status 400
    """

    mocked_repo.load_all_orders.return_value = test_order_status_2

    payment = Payment(**valid_payment)

    with pytest.raises(HTTPException) as exc_info:
        order_service.simulate_payment(test_order_status_2[0]["id"], payment)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == \
        f"Order {test_order_status_2[0]['id']} is not in a payable state"

def test_simulate_payment_invalid_card_number(mocked_repo,
                                              order_service,
                                              test_order_status,
                                              invalid_card_payment):
    """
    Spec: Method should reject payment if card number is invalid
    Input: valid order_id and invalid card number
    Expected behavior: HTTPException with status 400
    """

    mocked_repo.load_all_orders.return_value = test_order_status

    payment = Payment(**invalid_card_payment)

    with pytest.raises(HTTPException) as exc_info:
        order_service.simulate_payment(
            test_order_status[0]["id"],
            payment
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Payment Rejected: Invalid card number"

def test_simulate_payment_invalid_cvv(mocked_repo,
                                      order_service,
                                      test_order_status,
                                      invalid_cvv_payment):
    """
    Spec: Method should reject payment if CVV is invalid
    Input: valid order_id and invalid CVV
    Expected behavior: HTTPException raised and order not updated
    """

    mocked_repo.load_all_orders.return_value = test_order_status

    payment = Payment(**invalid_cvv_payment)

    with pytest.raises(HTTPException) as exc_info:
        order_service.simulate_payment(test_order_status[0]["id"], payment)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Payment Rejected: Invalid CVV"

def test_simulate_payment_expired_card(mocked_repo,
                                       order_service,
                                       test_order_status,
                                       expired_payment):
    """
    Spec: Method should reject payment if card is expired
    Input: valid order_id and expired card
    Expected behavior: HTTPException raised and order not updated
    """

    mocked_repo.load_all_orders.return_value = test_order_status

    payment = Payment(**expired_payment)

    with pytest.raises(HTTPException) as exc_info:
        order_service.simulate_payment(test_order_status[0]["id"], payment)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Payment Rejected: Card has expired"

def test_retry_payment_after_failure(mocked_repo,
                                     order_service,
                                     test_order_status,
                                     invalid_card_payment,
                                     valid_payment):
    """
    Spec: Customer should be able to retry payment after failure
    Input: invalid payment first, then valid payment
    Expected behavior: first attempt fails, second attempt succeeds
    """

    mocked_repo.load_all_orders.return_value = test_order_status

    # first attempt fails
    with pytest.raises(HTTPException) as exc_info:
        order_service.simulate_payment(
            test_order_status[0]["id"],
            Payment(**invalid_card_payment)
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Payment Rejected: Invalid card number"

    # second attempt succeeds
    result = order_service.simulate_payment(
        test_order_status[0]["id"],
        Payment(**valid_payment)
    )

    assert result.message == "Payment Accepted"
