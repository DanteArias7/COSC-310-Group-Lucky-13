# pylint: disable=redefined-outer-name

"""Tests for restaurant order management."""
import pytest
from fastapi import HTTPException
from app.services.restaurant_order_services import RestaurantOrderServices


@pytest.fixture
def sample_orders_data():
    """Sample orders for testing."""
    return [
        {
            "id": "order1",
            "restaurant_id": 101,
            "customer_id": "customer1",
            "assigned_driver_id": "",
            "food_items": "1x Burger",
            "order_date": "03-17-2026",
            "order_value": 15.99,
            "status": "Paid",
            "delivery_time": 0.0
        },
        {
            "id": "order2",
            "restaurant_id": 101,
            "customer_id": "customer2",
            "assigned_driver_id": "",
            "food_items": "2x Pizza",
            "order_date": "03-17-2026",
            "order_value": 25.99,
            "status": "Accepted_by_restaurant",
            "delivery_time": 0.0
        },
        {
            "id": "order3",
            "restaurant_id": 102,
            "customer_id": "customer3",
            "assigned_driver_id": "",
            "food_items": "1x Salad",
            "order_date": "03-17-2026",
            "order_value": 12.50,
            "status": "Paid",
            "delivery_time": 0.0
        }
    ]


@pytest.fixture
def mock_order_repo(mocker, sample_orders_data):
    """Mock order repository."""
    repo = mocker.Mock()
    repo.load_all_orders.return_value = sample_orders_data.copy()
    repo.update_orders.return_value = None
    return repo


@pytest.fixture
def restaurant_order_service(mock_order_repo):
    """Restaurant order service with mock repo."""
    return RestaurantOrderServices(mock_order_repo)


def test_get_restaurant_orders_success(restaurant_order_service):
    """Test getting all orders for a restaurant."""
    orders = restaurant_order_service.get_restaurant_orders(101)

    assert len(orders) == 2
    assert all(order.restaurant_id == 101 for order in orders)


def test_get_restaurant_orders_not_found(restaurant_order_service):
    """Test getting orders for restaurant with no orders."""
    with pytest.raises(HTTPException) as exc_info:
        restaurant_order_service.get_restaurant_orders(999)

    assert exc_info.value.status_code == 404


def test_get_restaurant_order_success(restaurant_order_service):
    """Test getting a specific order."""
    order = restaurant_order_service.get_restaurant_order(101, "order1")

    assert order.id == "order1"
    assert order.restaurant_id == 101


def test_get_restaurant_order_wrong_restaurant(restaurant_order_service):
    """Test getting order that belongs to different restaurant."""
    with pytest.raises(HTTPException) as exc_info:
        restaurant_order_service.get_restaurant_order(101, "order3")

    assert exc_info.value.status_code == 403


def test_accept_order_success(mocker, restaurant_order_service, mock_order_repo):
    """Test accepting an order."""
    # pylint: disable=unused-argument
    mock_notification = mocker.patch(
        "app.services.restaurant_order_services.send_notification"
    )
    mock_restaurant_repo = mocker.Mock()

    result = restaurant_order_service.accept_order(
        "order1", "owner1", mock_restaurant_repo
    )

    assert result.status == "Accepted_by_restaurant"
    mock_notification.assert_called_once()


def test_accept_order_wrong_status(mocker, restaurant_order_service):
    """Test accepting order that's not in Paid status."""
    mock_restaurant_repo = mocker.Mock()

    with pytest.raises(HTTPException) as exc_info:
        restaurant_order_service.accept_order(
            "order2", "owner1", mock_restaurant_repo
        )

    assert exc_info.value.status_code == 422


def test_update_status_to_preparing(restaurant_order_service):
    """Test updating from Accepted to Preparing."""
    result = restaurant_order_service.update_order_status(
        "order2", "Preparing", "owner1", None
    )

    assert result.status == "Preparing"


def test_update_status_to_ready(restaurant_order_service, mock_order_repo):
    """Test updating from Preparing to Ready_for_pickup."""
    # First update to Preparing
    orders = mock_order_repo.load_all_orders()
    orders[1]["status"] = "Preparing"
    mock_order_repo.load_all_orders.return_value = orders

    result = restaurant_order_service.update_order_status(
        "order2", "Ready_for_pickup", "owner1", None
    )

    assert result.status == "Ready_for_pickup"


def test_update_status_invalid_transition(restaurant_order_service):
    """Test invalid status transition."""
    with pytest.raises(HTTPException) as exc_info:
        restaurant_order_service.update_order_status(
            "order1", "Ready_for_pickup", "owner1", None
        )

    assert exc_info.value.status_code == 422
