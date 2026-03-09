"""Integration tests for order endpoints."""
from datetime import date
import json
from fastapi.testclient import TestClient
import pandas
import pytest
from app.main import app
from app.repositories.order_repo import OrderRepo
from app.repositories.user_repo import UserRepo
from app.routers.order import create_order_repo, create_user_repo


#pylint: disable=duplicate-code
#pylint: disable=redefined-outer-name

#Test Setup
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
                      "food_items": "2x Vegan Burger, 1x Bacon Burger",
                      "order_date": "03-06-2025",
                      "order_value": 24.35,
                      "status": "Pending"},
                      {"id": "QQQQQQQ",
                      "restaurant_id": 101,
                      "customer_id": "00000000-0000-0000-0000-000000000001",
                      "food_items": "2x Vegan Burger",
                      "order_date": "03-06-2025",
                      "order_value": 24.35,
                      "status": "Pending"},
                      {"id": "QQQQQQQ",
                      "restaurant_id": 101,
                      "customer_id": "00000000-0000-0000-0000-000000000002",
                      "food_items": "1x Hot Dog",
                      "order_date": "03-06-2025",
                      "order_value": 24.35,
                      "status": "Pending"}
                      ]

@pytest.fixture
def test_users():
    """Initialize test user data for each test"""
    return [{"id": "00000000-0000-0000-0000-000000000001",
            "name": "Alex",
            "email": "alexsmith@gmail.com",
            "phone_number": "123-456-7890",
            "address": "123 Baron Rd, Kelowna, BC, A1B2C3",
            "password": "password",
            "role": "customer"},
            {"id": "00000000-0000-0000-0000-000000000002",
            "name": "Alex",
            "email": "alexsmith@gmail.com",
            "phone_number": "123-456-7890",
            "address": "123 Baron Rd, Kelowna, BC, A1B2C3",
            "password": "password",
            "role": "restaurant_owner"},
            {"id": "00000000-0000-0000-0000-000000000003",
            "name": "Alex",
            "email": "alexsmith@gmail.com",
            "phone_number": "123-456-7890",
            "address": "123 Baron Rd, Kelowna, BC, A1B2C3",
            "password": "password",
            "role": "customer"}]


@pytest.fixture
def temp_order_path(tmp_path, test_orders):
    """Create temporary cart file path for each test"""
    test_order_data_path = tmp_path / "order.csv"

    headersdf = pandas.DataFrame(columns=["id",
                                        "restaurant_id",
                                        "customer_id",
                                        "food_items",
                                        "order_date",
                                        "order_value",
                                        "status"])

    headersdf.to_csv(test_order_data_path, index=False)

    orderdf = pandas.DataFrame(test_orders)
    orderdf.to_csv(test_order_data_path, mode='a', index=False, header=False)

    return test_order_data_path

@pytest.fixture
def temp_user_path(tmp_path, test_users):
    """Create temporary user file path for each test"""
    test_user_data_path = tmp_path / "users.json"

    with open(test_user_data_path, "w", encoding="utf-8") as f:
        json.dump(test_users, f, ensure_ascii=False)

    return test_user_data_path

@pytest.fixture
def order_test_client(temp_user_path, temp_order_path):
    """Override dependency injection for restaurant repo object"""

    def override_order_repo():
        return OrderRepo(temp_order_path)

    def override_user_repo():
        return UserRepo(temp_user_path)

    app.dependency_overrides[create_order_repo] = override_order_repo
    app.dependency_overrides[create_user_repo] = override_user_repo

    yield TestClient(app)

    app.dependency_overrides.clear()

#add_order
def test_add_order_success(temp_order_path,
                             order_test_client, test_carts,
                             test_users):
    """Scenario: Test succesful endpoint use to create an order"""

    payload = test_carts[0]

    request = "/orders/"

    r =order_test_client.post(request, headers={"user-id" : test_users[0]["id"]},
                           json=payload)

    orders = pandas.read_csv(temp_order_path)

    new_order = orders.tail(1).to_dict(orient="records")[0]

    del new_order["id"]

    expected_order = {
                      "restaurant_id": 101,
                      "customer_id": "00000000-0000-0000-0000-000000000001",
                      "food_items": "2x Vegan Burger, 1x Bacon Burger",
                      "order_date": date.today().strftime("%m-%d-%Y"),
                      "order_value": 24.35,
                      "status": "Pending"}

    assert r.status_code == 201
    assert new_order == expected_order

#get_order_by_user_id Tests
def test_get_order_by_user_id_success(order_test_client, test_orders,
                             test_users):
    """
    Spec: System should allow user to retrieve their own orders
    Input: valid user_id
    Expected behavior: Endpoint returns list of user orders
    """

    r = order_test_client.get("/orders", headers={"user-id" : test_users[0]["id"]})

    expected_orders = [test_orders[0], test_orders[1]]

    user_orders = r.json()

    assert r.status_code == 200
    assert user_orders == expected_orders

def test_get_order_by_user_id_with_no_orders(order_test_client,
                             test_users):
    """
    Spec: System should return error if user with no orders attempts to get order
    Input: valid user_id that does not have any orders
    Expected behavior: Method raises 404 HTTPException
    """

    r = order_test_client.get("/orders", headers={"user-id" : test_users[2]["id"]})

    assert r.status_code == 404

#simulate_payment Tests
def test_simulate_payment_success(temp_order_path,
                                  order_test_client,
                                  test_orders,
                                  test_users):
    """
    Spec: System should simulate payment for an order
    Input: valid order_id
    Expected behavior: Order status should update to Paid
    """

    order_id = test_orders[0]["id"]

    request = f"/orders/{order_id}/simulate-payment"

    r = order_test_client.post(request,
                               headers={"user-id": test_users[0]["id"]})

    orders = pandas.read_csv(temp_order_path)

    updated_order = orders.iloc[0].to_dict()

    assert r.status_code == 200
    assert updated_order["status"] == "Paid"

def test_simulate_payment_order_not_found(order_test_client,
                                          test_users):
    """
    Spec: System should return error if order does not exist
    Input: invalid order_id
    Expected behavior: Method raises 404 HTTPException
    """

    request = "/orders/INVALIDID/simulate-payment"

    r = order_test_client.post(request,
                               headers={"user-id": test_users[0]["id"]})

    assert r.status_code == 404

def test_simulate_payment_invalid_status(temp_order_path,
                                         order_test_client,
                                         test_orders,
                                         test_users):
    """
    Spec: System should prevent payment if order is not in Pending status
    Input: valid order_id with status not Pending
    Expected behavior: Endpoint returns 400 error
    """

    orders = pandas.read_csv(temp_order_path)

    # change status to Paid to simulate invalid state
    orders.loc[0, "status"] = "Paid"

    orders.to_csv(temp_order_path, index=False)

    order_id = test_orders[0]["id"]

    request = f"/orders/{order_id}/simulate-payment"

    r = order_test_client.post(request,
                               headers={"user-id": test_users[0]["id"]})

    assert r.status_code == 400
