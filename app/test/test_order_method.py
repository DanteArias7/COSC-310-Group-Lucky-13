"""Tests for restaurant functionality."""
from fastapi import HTTPException
import pytest
from app.schemas.cart import Cart
from app.schemas.payment import Payment
from app.services.order_services import OrderServices



#pylint: disable=redefined-outer-name
#pylint: disable=duplicate-code
#pylint: disable=too-few-public-methods
#pylint: disable=too-many-arguments
#pylint: disable=too-many-positional-arguments
@pytest.fixture
def mocked_repo(mocker):
    """Creates a mocked repo object for each test"""
    return mocker.Mock()

@pytest.fixture
def order_service(mocked_repo):
    """Creates a restaurant service object with mocked repo"""
    return OrderServices(mocked_repo, mocked_repo)

@pytest.fixture
def test_carts():
    """Initialize Test cart data for each test"""
    return [{"id" : "00000000-0000-0000-0000-000000000001",
            "user_id" : "00000000-0000-0000-0000-000000000001",
            "restaurant_id" : 101,
            "cart_items" :  [{"item": {"id": "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01",
                            "name": "Vegan Burger",
                            "description": "Plant-based patty with lettuce and tomato",
                            "price": 12.50,
                            "tags": ["vegan"]},
                            "quantity": 2,
                            "status": "Available"},
                            {"item": {"id": "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01",
                            "name": "Bacon Burger",
                            "description": "Burger with bacon",
                            "price": 10.50,
                            "tags": ["vegan"]},
                            "quantity": 1,
                            "status": "Available"}],
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
         "assigned_driver_id": "",
         "food_items": "1x Burger",
         "order_date": "03-06-2026",
         "order_value": 12.50,
         "status": "Pending",
         "delivery_time": 0.0}]

@pytest.fixture
def test_order_status_2():
    """Initialize test order data with status for payment tests"""
    return[{"id": "BBBBBBB",
         "restaurant_id": 101,
         "customer_id": "00000000-0000-0000-0000-000000000001",
         "assigned_driver_id": "",
         "food_items": "1x Burger",
         "order_date": "03-06-2026",
         "order_value": 12.50,
         "status": "Paid",
         "delivery_time": 0.0}]

@pytest.fixture
def valid_payment():
    """Valid Visa/Mastercard payment payload"""
    return {
        "user_id" : "00000000-0000-0000-0000-000000000001",
        "card_number": "1234567812345678",
        "cvv": "123",
        "expiration_date": "12/30"
    }

@pytest.fixture
def valid_payment_amex():
    """Valid Amex payment payload"""
    return {
        "user_id" : "00000000-0000-0000-0000-000000000001",
        "card_number": "123456781234567",
        "cvv": "1234",
        "expiration_date": "12/30"
    }

@pytest.fixture
def amex_card_invalid_cvv():
    """Sample Amex payment details with invalid CVV for payment simulation tests"""
    return {
        "user_id" : "00000000-0000-0000-0000-000000000001",
        "card_number": "123456781234567",
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

@pytest.fixture
def test_orders_available():
    """Orders with correct statuses for available delivery tests"""
    return [
        {"id": "AAAAAAA",
            "restaurant_id": 101,
            "customer_id": "00000000-0000-0000-0000-000000000001",
            "assigned_driver_id": "",
            "food_items": "2x Vegan Burger",
            "order_date": "03-16-2026",
            "order_value": 24.35,
            "status": "Accepted_by_restaurant",
            "delivery_time": 0.0},
        {"id": "BBBBBBB",
            "restaurant_id": 101,
            "customer_id": "00000000-0000-0000-0000-000000000001",
            "assigned_driver_id": "",
            "food_items": "1x Hot Dog",
            "order_date": "03-16-2026",
            "order_value": 10.00,
            "status": "Preparing",
            "delivery_time": 0.0},
        {"id": "CCCCCCC",
            "restaurant_id": 101,
            "customer_id": "00000000-0000-0000-0000-000000000001",
            "assigned_driver_id": "00000001-0000-0000-0000-000000000000",
            "food_items": "1x Salad",
            "order_date": "03-16-2026",
            "order_value": 8.00,
            "status": "Ready_for_pickup",
            "delivery_time": 0.0}
    ]

@pytest.fixture
def test_orders_paid():
    """Orders in Paid status for pending paid order tests"""
    return [
        {"id": "DDDDDDD",
            "restaurant_id": 101,
            "customer_id": "00000000-0000-0000-0000-000000000001",
            "assigned_driver_id": "",
            "food_items": "2x Vegan Burger",
            "order_date": "03-16-2026",
            "order_value": 24.35,
            "status": "Paid",
            "delivery_time": 0.0},
        {"id": "EEEEEEE",
            "restaurant_id": 101,
            "customer_id": "00000000-0000-0000-0000-000000000002",
            "assigned_driver_id": "",
            "food_items": "1x Hot Dog",
            "order_date": "03-16-2026",
            "order_value": 10.00,
            "status": "Pending",
            "delivery_time": 0.0}
    ]

@pytest.fixture
def test_orders_assigned():
    """Orders with assigned driver for assigned order tests"""
    return [
        {"id": "FFFFFFF",
            "restaurant_id": 101,
            "customer_id": "00000000-0000-0000-0000-000000000001",
            "assigned_driver_id": "00000001-0000-0000-0000-000000000000",
            "food_items": "2x Vegan Burger",
            "order_date": "03-16-2026",
            "order_value": 24.35,
            "status": "In_transit",
            "delivery_time": 0.0},
        {"id": "GGGGGGG",
            "restaurant_id": 101,
            "customer_id": "00000000-0000-0000-0000-000000000002",
            "assigned_driver_id": "00000002-0000-0000-0000-000000000000",
            "food_items": "1x Hot Dog",
            "order_date": "03-16-2026",
            "order_value": 10.00,
            "status": "In_transit",
            "delivery_time": 0.0}
    ]

#place_order Unit Tests
def test_place_order_success(mocker, mocked_repo, order_service, test_carts):
    """Scenario: check that creating a valid order returns a valid order object
       and generates a notification"""

    mocked_random = "Q"
    id_mock = mocker.patch("app.services.order_services.random.choice")
    id_mock.return_value = mocked_random

    notification_mock = mocker.patch(
        "app.services.order_services.send_notification"
    )

    test_date = "03-06-2026"
    mocked_date = mocker.patch("app.services.order_services.date")
    mocked_date.today.return_value.strftime.return_value = test_date

    mocked_repo.save_order.return_value = None

    cart = Cart(**test_carts[0])

    order = order_service.place_order(cart)

    expected_order = {"id": "QQQQQQQ",
                      "restaurant_id": 101,
                      "customer_id": "00000000-0000-0000-0000-000000000001",
                      "assigned_driver_id": "",
                      "food_items": "2x Vegan Burger, 1x Bacon Burger",
                      "order_date": test_date,
                      "order_value": 24.35,
                      "status": "Pending",
                      "delivery_time": 0.0}

    assert order.model_dump() == expected_order

    notification_mock.assert_called_once()

    notification_obj = notification_mock.call_args[0][0]

    assert notification_obj.user_id == cart.user_id
    assert notification_obj.message == (
        f"Your order {expected_order['id']} "
        "has been created successfully"
    )

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

#get_order_by_restaurant_id Unit Tests
def test_get_order_by_restaurant_id_success(mocked_repo, order_service, test_orders):
    """
    Spec: Method should return orders for a restaurant
    Input: valid restaurant ID
    Expected behavior: Method returns List of order objects
    """
    mocked_repo.load_all_orders.return_value = test_orders

    orders = order_service.get_past_orders_by_restaurant_id(test_orders[0]["restaurant_id"])

    expected_orders = [test_orders[0], test_orders[1], test_orders[2]]

    assert orders == expected_orders

#simulate_payment Unit Tests
def test_simulate_payment_success(mocked_repo, order_service, test_order_status,
                                  valid_payment, mocker):
    """
    Spec: Method should simulate payment for an order and update order status to Paid
    Input: valid order_id and valid payment details
    Expected behavior: Order status should update to Paid &&
                        method should return payment result message
    """

    mock_send = mocker.patch("app.services.order_services.send_notification")

    mocked_repo.load_all_orders.return_value = test_order_status
    mocked_repo.update_orders.return_value = None

    mock_restaurant_obj = mocker.Mock()
    mock_restaurant_obj.user_id = "owner-123"

    order_service.restaurant_service.fetch_restaurant = mocker.Mock(
        return_value=mock_restaurant_obj
    )

    payment = Payment(**valid_payment)

    result = order_service.simulate_payment(
        test_order_status[0]["id"],
        payment
    )

    assert result.message == "Payment Accepted"
    assert test_order_status[0]["status"] == "Paid"
    assert mock_send.call_count == 2

    calls = mock_send.call_args_list

    customer_notification = calls[0][0][0]
    owner_notification = calls[1][0][0]

    assert customer_notification.user_id == test_order_status[0]["customer_id"]
    assert customer_notification.message == (
        f"Your order {test_order_status[0]['id']} has been paid successfully"
    )

    assert owner_notification.user_id == "owner-123"
    assert owner_notification.message == (
        f"You have received a new order {test_order_status[0]['id']}"
    )

def test_simulate_payment_amex(mocked_repo, order_service,
                                           test_order_status, valid_payment_amex, mocker):
    """Spec: Method should simulate payment for an order and update order status to Paid
    Input: valid order_id and valid Amex payment details
    Expected behavior: Order status should update to Paid &&
                        method should return payment result message
    """
    mocked_repo.load_all_orders.return_value = test_order_status

    mock_restaurant_obj = mocker.Mock()
    mock_restaurant_obj.user_id = "owner-123"

    order_service.restaurant_service.fetch_restaurant = mocker.Mock(
        return_value=mock_restaurant_obj
    )

    payment = Payment(**valid_payment_amex)

    result = order_service.simulate_payment(
        test_order_status[0]["id"],
        payment
    )

    assert result.message == "Payment Accepted"
    assert test_order_status[0]["status"] == "Paid"

def test_simulate_payment_amex_invalid_cvv(mocked_repo, order_service ,
                                           test_order_status, amex_card_invalid_cvv):
    """
    Spec: Method should reject payment if CVV is invalid
    Input: valid order_id and invalid Amex CVV
    Expected behavior: HTTPException with status 400
    """
    mocked_repo.load_all_orders.return_value = test_order_status

    payment = Payment(**amex_card_invalid_cvv)

    with pytest.raises(HTTPException) as exc_info:
        order_service.simulate_payment(test_order_status[0]["id"], payment)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Payment Rejected: Invalid CVV"


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
                                     valid_payment, mocker):
    """
    Spec: Customer should be able to retry payment after failure
    Input: invalid payment first, then valid payment
    Expected behavior: first attempt fails, second attempt succeeds
    """

    mocked_repo.load_all_orders.return_value = test_order_status

    with pytest.raises(HTTPException) as exc_info:
        order_service.simulate_payment(
            test_order_status[0]["id"],
            Payment(**invalid_card_payment)
        )
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Payment Rejected: Invalid card number"

    # second attempt succeeds

    mock_restaurant_obj = mocker.Mock()
    mock_restaurant_obj.user_id = "owner-123"

    order_service.restaurant_service.fetch_restaurant = mocker.Mock(
        return_value=mock_restaurant_obj
    )

    result = order_service.simulate_payment(
        test_order_status[0]["id"],
        Payment(**valid_payment)
    )

    assert result.message == "Payment Accepted"

def test_notify_restaurant_owner_success(order_service, test_order_status_2, mocker):
    """
    Spec: Method should send notification to restaurant owner when a new order is placed
    Input: valid restaurant_id and order_id
    Expected behavior: send_notification should be called with correct notification object
    """

    restaurant = test_order_status_2[0]

    mock_send = mocker.patch("app.services.order_services.send_notification")

    order_service.restaurant_service.fetch_restaurant = mocker.Mock(
        return_value=mocker.Mock(user_id="owner-123")
    )

    order_service.notify_restaurant_owner(
        restaurant["restaurant_id"],
        restaurant["id"]
    )

    mock_send.assert_called_once()

    notification = mock_send.call_args[0][0]

    assert notification.user_id == "owner-123"
    assert notification.message == (
        f"You have received a new order {restaurant['id']}"
    )

def test_notify_restaurant_owner_restaurant_not_found(mocker, order_service):
    """
    Spec: Method should raise exception if restaurant does not exist
    Input: invalid restaurant_id
    Expected behavior: HTTPException with status 404
    """

    restaurant_id = 999
    order_id = "ORDER123"

    order_service.restaurant_service.fetch_restaurant = mocker.Mock(
        return_value=None
    )

    with pytest.raises(HTTPException) as exc_info:
        order_service.notify_restaurant_owner(restaurant_id, order_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f"Restaurant {restaurant_id} Not Found"

#get_all_available_delivery_orders Unit tests
def test_get_all_available_delivery_orders_success(mocked_repo,
                                                   order_service,
                                                   test_orders_available):
    """
    Spec: Method should return orders that are available for pickup
    Input: orders with correct statuses and no assigned driver
    Expected behavior: Returns only unassigned orders with valid statuses
    """
    mocked_repo.load_all_orders.return_value = test_orders_available

    result = order_service.get_all_available_delivery_orders()

    assert len(result) == 2
    assert all(order.assigned_driver_id == "" for order in result)
    assert all(order.status in ("Accepted_by_restaurant", "Preparing", "Ready_for_pickup")
               for order in result)

def test_get_all_available_delivery_orders_none_found(mocked_repo, order_service):
    """
    Spec: Method should return empty list if no available orders exist
    Input: empty order list
    Expected behavior: Returns empty list
    """
    mocked_repo.load_all_orders.return_value = []

    result = order_service.get_all_available_delivery_orders()

    assert result == []

def test_get_available_orders_success(mocked_repo, order_service, test_orders):
    """Test driver can see available orders."""
    test_orders[0]["status"] = "Ready_for_pickup"
    test_orders[0]["assigned_driver_id"] = ""
    mocked_repo.load_all_orders.return_value = test_orders

    result = order_service.get_available_orders()

    assert len(result) == 1
    assert result[0].status == "Ready_for_pickup"
    assert not result[0].assigned_driver_id


def test_get_available_orders_empty(mocked_repo, order_service, test_orders):
    """Test when no orders are available."""
    test_orders[0]["status"] = "Preparing"
    mocked_repo.load_all_orders.return_value = test_orders

    result = order_service.get_available_orders()
    assert result == []


def test_accept_delivery_success(mocker, mocked_repo, order_service, test_orders):
    """Test driver successfully accepts an order."""
    mock_notification = mocker.patch(
        "app.services.order_services.send_notification"
    )

    test_orders[0]["status"] = "Ready_for_pickup"
    test_orders[0]["assigned_driver_id"] = ""
    mocked_repo.load_all_orders.return_value = test_orders

    result = order_service.accept_delivery(test_orders[0]["id"], "driver123")

    assert result.status == "Ready_for_pickup"
    assert result.assigned_driver_id == "driver123"
    mock_notification.assert_called_once()


def test_accept_delivery_not_ready(mocked_repo, order_service, test_orders):
    """Test cannot accept order not in Ready_for_pickup status."""
    test_orders[0]["status"] = "Preparing"
    test_orders[0]["assigned_driver_id"] = ""
    mocked_repo.load_all_orders.return_value = test_orders

    with pytest.raises(HTTPException) as exc_info:
        order_service.accept_delivery(test_orders[0]["id"], "driver123")

    assert exc_info.value.status_code == 422
    assert "not ready for pickup" in exc_info.value.detail


def test_accept_delivery_already_assigned(mocked_repo, order_service, test_orders):
    """Test cannot accept order already assigned."""
    test_orders[0]["status"] = "Ready_for_pickup"
    test_orders[0]["assigned_driver_id"] = "other_driver"
    mocked_repo.load_all_orders.return_value = test_orders

    with pytest.raises(HTTPException) as exc_info:
        order_service.accept_delivery(test_orders[0]["id"], "driver123")

    assert exc_info.value.status_code == 409
    assert "already assigned" in exc_info.value.detail
