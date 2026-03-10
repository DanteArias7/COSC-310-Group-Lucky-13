"""Integration tests for restaurant endpoints."""
from datetime import date
import json
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.repositories.cart_repo import CartRepo
from app.repositories.restaurant_repo import RestaurantRepo
from app.repositories.user_repo import UserRepo
from app.routers.restaurant import create_cart_repo, create_restaurant_repo, create_user_repo

#pylint: disable=duplicate-code
#pylint: disable=redefined-outer-name

#Test Setup
@pytest.fixture
def test_restaurants():
    """Initialize test restaurant data for each test"""
    return [{"id": 101,
             "user_id" : "00000000-0000-0000-0000-000000000002",
               "name": "Veggie Palace",
                "hours": { "Monday": "9:00-17:00",
                            "Tuesday": "9:00-17:00",
                            "Wednesday": "9:00-17:00",
                            "Thursday": "9:00-17:00",
                            "Friday": "9:00-17:00",
                            "Saturday": "9:00-17:00",
                            "Sunday": "9:00-17:00"},
                "phone_number": "1234567890",
                "address": "123 Green Street",
                "tags": ["vegan", "brunch"],
                "menu": [{"id": "00000000-0000-0000-0000-0000000000001",
                "name": "Vegan Burger", "description": "Plant-based patty with lettuce and tomato",
                "price": 12.99, "tags": ["vegan"]
                }]
        }]

@pytest.fixture
def test_carts():
    """Initialize test cart data for each test"""
    return [{"id" : "00000000-0000-0000-0000-000000000001",
            "user_id" : "00000000-0000-0000-0000-000000000001",
            "restaurant_id" : 101,
            "cart_items" :  [{"item": {"id": "018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01",
                            "name": "Vegan Burger",
                            "description": "Plant-based patty with lettuce and tomato",
                            "price": 12.99,
                            "tags": ["vegan"]},
                            "quantity": 1}],
                "subtotal" : 12.99,
                "tax" : 1.30,
                "total" : 14.29}]

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
            "role": "restaurant_owner"}]

@pytest.fixture
def temp_restaurant_path(tmp_path, test_restaurants):
    """Create temporary restaurant file path for each test"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    return test_restaurant_data_path

@pytest.fixture
def temp_cart_path(tmp_path, test_carts):
    """Create temporary cart file path for each test"""
    test_cart_data_path = tmp_path / "carts.json"

    with open(test_cart_data_path, "w", encoding="utf-8") as f:
        json.dump(test_carts, f, ensure_ascii=False)

    return test_cart_data_path

@pytest.fixture
def temp_user_path(tmp_path, test_users):
    """Create temporary user file path for each test"""
    test_user_data_path = tmp_path / "users.json"

    with open(test_user_data_path, "w", encoding="utf-8") as f:
        json.dump(test_users, f, ensure_ascii=False)

    return test_user_data_path

@pytest.fixture
def restaurant_test_client(temp_user_path, temp_restaurant_path):
    """Override dependency injection for restaurant repo object"""

    def override_restaurant_repo():
        return RestaurantRepo(temp_restaurant_path)

    def override_user_repo():
        return UserRepo(temp_user_path)

    app.dependency_overrides[create_restaurant_repo] = override_restaurant_repo
    app.dependency_overrides[create_user_repo] = override_user_repo

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def cart_test_client(temp_user_path, temp_cart_path):
    """Override dependency injection for restaurant repo object"""

    def override_restaurant_repo():
        return CartRepo(temp_cart_path)

    def override_user_repo():
        return UserRepo(temp_user_path)

    app.dependency_overrides[create_cart_repo] = override_restaurant_repo
    app.dependency_overrides[create_user_repo] = override_user_repo

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def menu_item_payload():
    """Sample menu item payload for cart tests"""
    return {
        "id": "new-item",
        "name": "Fries",
        "description": "Crispy",
        "price": 5.00,
        "tags": ["fries"]
    }

#get_all_restaurants Integration Tests

def test_get_all_restaurants_integration(restaurant_test_client, temp_restaurant_path,
                                         test_users):
    """Test retrieving all restaurants via GET /restaurants/."""

    response = restaurant_test_client.get("/restaurants/", headers={"user-id": test_users[1]["id"]})

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    restaurant = data[0]
    today = date.today().strftime("%A")

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert restaurants[0]["id"] == data[0]["id"]
    assert restaurants[0]["name"] == data[0]["name"]
    assert restaurants[0]["address"] == data[0]["address"]
    assert restaurants[0]["hours"][today] == data[0]["todays_hours"]
    assert restaurants[0]["tags"] == data[0]["tags"]

    assert isinstance(restaurant["todays_hours"], str)
    assert isinstance(restaurant["tags"], list)

#get_restaurant_by_id Integration Tests

def test_get_single_restaurant_integration(test_restaurants, test_users,
                                            restaurant_test_client, temp_restaurant_path):
    """Test retrieving a single restaurant via GET /restaurants/{id}."""

    request = "/restaurants/" + str(test_restaurants[0]["id"])
    response = restaurant_test_client.get(request, headers={"user-id": test_users[1]["id"]})

    assert response.status_code == 200
    data = response.json()

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert restaurants[0] == data

    assert isinstance(data["tags"], list)
    assert isinstance(data["menu"], list)

def test_get_nonexistent_restaurant_integration(restaurant_test_client, test_users):
    """Test retrieving a restaurant that does not exist."""

    response = restaurant_test_client.get("/restaurants/103",
                                        headers={"user-id": test_users[1]["id"]})

    assert response.status_code == 404

#create_restaurant Integration Tests

def test_create_restaurant_integration(restaurant_test_client, temp_restaurant_path,
                                        test_users):
    """Test creating a restaurant via POST /restaurants"""

    payload = {
        "user_id" : "00000000-0000-0000-0000-000000000001",
        "name": "Taco Town",
        "hours": {"Monday": "10:00-20:00"},
        "phone_number": "5555555555",
        "address": "123 Taco Lane",
        "tags": ["mexican"],
        "menu": [
            {
                "id": "00000000-0000-0000-0000-000000000011",
                "name": "Taco",
                "description": "Beef taco",
                "price": 5.0,
                "tags": ["mexican"]
            }
        ]
    }

    r = restaurant_test_client.post("/restaurants",
                                    headers={"user-id": test_users[1]["id"]}, json=payload)
    print(r.json)
    assert r.status_code == 201

    data = r.json()

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert data == restaurants[1]

def test_create_restaurant_without_menu_integration(restaurant_test_client, test_users):
    """Restaurant cannot be created without menu items"""

    payload = {
        "name": "Taco Town",
        "hours": {"Monday": "10:00-20:00"},
        "phone_number": "5555555555",
        "address": "123 Taco Lane",
        "tags": ["mexican"],
        "menu": []
    }

    r = restaurant_test_client.post("/restaurants",
                                    headers={"user-id": test_users[1]["id"]}, json=payload)

    assert r.status_code == 422

#update_restaurant Integration Tests

def test_updating_restaurant_successful(test_restaurants, restaurant_test_client,
                                         temp_restaurant_path, test_users):
    """Testing successful updating of a restaurants information"""

    payload = {"name": "Meat Palace",
                "hours": {"Monday": "9:00-2:00"}, "phone_number": "9876543210",
                "address": "321 Red Street",
                "tags": ["brunch"]}

    request = "/restaurants/" + str(test_restaurants[0]["id"])
    r = restaurant_test_client.put(request, headers= {"user-id" : test_users[1]["id"]},
                                    json=payload)

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    test_restaurants[0]["name"] = "Meat Palace"
    test_restaurants[0]["hours"] = {"Monday" : "9:00-2:00"}
    test_restaurants[0]["phone_number"] = "9876543210"
    test_restaurants[0]["address"] = "321 Red Street"
    test_restaurants[0]["tags"] = ["brunch"]

    assert r.status_code == 200
    assert restaurants == test_restaurants

def test_updating_nonexistent_restaurant(test_restaurants, restaurant_test_client,
                                          temp_restaurant_path, test_users):
    """Testing unsuccesful updating of a resturant that does not exist"""

    payload = {"name": "Meat Palace",
                "hours": {"Monday": "9:00-2:00"}, "phone_number": "9876543210",
                "address": "321 Red Street",
                "tags": ["brunch"]}

    r = restaurant_test_client.put("/restaurants/999", headers= {"user-id" : test_users[1]["id"]},
                                    json=payload)


    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

#delete_restaurant Integration Tests

def test_delete_restaurant_successful(test_restaurants, restaurant_test_client,
                                       temp_restaurant_path, test_users):
    """Testing successful deletion of a restaurants information"""

    request = "/restaurants/" + str(test_restaurants[0]["id"])
    r = restaurant_test_client.delete(request, headers= {"user-id" : test_users[1]["id"]})


    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 204
    assert restaurants == []

def test_delete_nonexistent_restaurant(test_restaurants, restaurant_test_client,
                                        temp_restaurant_path, test_users):
    """Testing unsuccessful deletion of a restaurants information"""

    r = restaurant_test_client.delete("/restaurants/999",
                                      headers= {"user-id" : test_users[1]["id"]})

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

#add_menu_item_to_menu Integration Tests

def test_adding_menu_item(test_restaurants, restaurant_test_client,
                          temp_restaurant_path, test_users):
    """Testing adding a menu item to a restaurant's menu"""

    payload = {"name": "Classic Burger",
                "description": "Cheeseburger", "price": 10.50, "tags": ["burger"]}

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + "/menu"
    r = restaurant_test_client.post(request, headers= {"user-id" : test_users[1]["id"]},
                                    json=payload)

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    menu_item = r.json()

    test_restaurants[0]["menu"].append(menu_item)

    assert r.status_code == 201
    assert restaurants == test_restaurants

def test_adding_menu_item_already_exists(test_restaurants, restaurant_test_client,
                                         temp_restaurant_path, test_users):
    """Testing adding a menu item that already exists in a restaurant's menu"""

    payload = {"name": "Vegan Burger",
                "description": "Cheeseburger", "price": 10.50, "tags": ["burger"]}

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + "/menu"
    r = restaurant_test_client.post(request, headers= {"user-id" : test_users[1]["id"]},
                                    json=payload)

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 409
    assert restaurants == test_restaurants

def test_adding_menu_item_nonexistent_restaurant(test_restaurants, restaurant_test_client,
                                                  temp_restaurant_path, test_users):
    """Testing adding a menu item to a restaurant that does not exist"""

    payload = {"name": "Vegan Burger",
                "description": "Cheeseburger", "price": 10.50, "tags": ["burger"]}

    r = restaurant_test_client.post("/restaurants/999/menu",
                                    headers= {"user-id" : test_users[1]["id"]},
                                    json=payload)

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants


#update_menu_item_in_menu Integration Tests

def test_updating_menu_item_successful(test_restaurants, restaurant_test_client,
                                       temp_restaurant_path, test_users):
    """Testing successful updating of a menu item to a menu"""

    payload = {"name": "Hot Dog", "description": "Beef hot dog on bun",
                "price": 5.99, "tags": ["beef"]}

    request = "/restaurants/" + str(test_restaurants[0]["id"])
    request = request + "/menu/" + test_restaurants[0]["menu"][0]["id"]
    r = restaurant_test_client.put(request, headers= {"user-id" : test_users[1]["id"]},
                                    json=payload)


    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    test_restaurants[0]["menu"][0]["name"] = "Hot Dog"
    test_restaurants[0]["menu"][0]["description"] = "Beef hot dog on bun"
    test_restaurants[0]["menu"][0]["price"] = 5.99
    test_restaurants[0]["menu"][0]["tags"] = ["beef"]

    assert r.status_code == 200
    assert restaurants == test_restaurants

def test_updating_nonexistent_menu_item(test_restaurants, restaurant_test_client,
                                        temp_restaurant_path, test_users):
    """Testing unsuccessful updating of a menu item that does not exist"""

    payload = {"name": "Hot Dog", "description": "Beef hot dog on bun",
                "price": 5.99, "tags": ["beef"]}

    request = "/restaurants/" + str(test_restaurants[0]["id"])
    request = request + "/menu/99999999-9999-9999-9999-999999999999"
    r = restaurant_test_client.put(request, headers= {"user-id" : test_users[1]["id"]},
                                    json=payload)

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_updating_menu_item_to_nonexistent_restaurant(test_restaurants,restaurant_test_client,
                                                      temp_restaurant_path, test_users):
    """Testing unsuccessful updating of a menu item to restaurant that does not exist"""

    payload = {"name": "Hot Dog", "description": "Beef hot dog on bun",
                "price": 5.99, "tags": ["beef"]}

    request = "/restaurants/999/menu/99999999-9999-9999-9999-999999999999"
    r = restaurant_test_client.put(request, headers= {"user-id" : test_users[1]["id"]},
                                    json=payload)

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

#delete_menu_item_from_menu Integration Tests

def test_deleting_menu_item_success(test_restaurants, restaurant_test_client,
                                    temp_restaurant_path, test_users):
    """Testing a successful deleting of a menu item"""

   # Appending a second menu item so deletion is allowed as empty menus are not allowed
    test_restaurants[0]["menu"].append({
        "id": "00000000-0000-0000-0000-0000000000002",
        "name": "Fries",
        "description": "Yam Fries",
        "price": 5.99,
        "tags": ["fries"]
    })

    with open(temp_restaurant_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    request = "/restaurants/" + str(test_restaurants[0]["id"])
    request = request + "/menu/" + test_restaurants[0]["menu"][0]["id"]
    r = restaurant_test_client.delete(request, headers= {"user-id" : test_users[1]["id"]})

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 204
    assert len(restaurants[0]["menu"]) == 1
    assert restaurants[0]["menu"][0]["id"] == "00000000-0000-0000-0000-0000000000002"

def test_deleting_menu_item_to_nonexistent_restaurant(test_restaurants, restaurant_test_client,
                                                      temp_restaurant_path, test_users):
    """Testing unsuccessful deleting of menu item from a restaurant that does not exist"""

    request = "/restaurants/999/menu/" + test_restaurants[0]["menu"][0]["id"]
    r = restaurant_test_client.delete(request, headers= {"user-id" : test_users[1]["id"]})

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_deleting_nonexistent_menu_item(test_restaurants, test_users,
                                        restaurant_test_client, temp_restaurant_path):
    """Testing unsuccessful deleting of a menu item that does not exist"""

    request = "/restaurants/" + str(test_restaurants[0]["id"])
    request = request + "/menu/99999999-9999-9999-9999-999999999999"
    r = restaurant_test_client.delete(request, headers= {"user-id" : test_users[1]["id"]})

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_deleting_last_menu_item_fails(test_restaurants,test_users,
                                       restaurant_test_client, temp_restaurant_path):
    """Testing unsuccessful deletion of the last remaining menu item"""

    request = "/restaurants/" + str(test_restaurants[0]["id"])
    request = request + "/menu/" + test_restaurants[0]["menu"][0]["id"]
    r = restaurant_test_client.delete(request, headers= {"user-id" : test_users[1]["id"]})

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 400
    assert restaurants == test_restaurants


#add_user_cart_for_a_restaurant Integration tests

def test_add_user_cart_for_a_restaurant_success(test_carts, test_users,
                                           cart_test_client, temp_cart_path ,
                                           menu_item_payload):
    """Testing successful addition of item to a user's cart"""

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart"

    r = cart_test_client.post(request, json=menu_item_payload,
                              headers= {"user-id" : test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    test_carts[0]["cart_items"] = []
    test_carts[0]["tax"] = 0.00
    test_carts[0]["subtotal"] = 0.00
    test_carts[0]["total"] = 0.00

    test_carts[0]["id"] = carts[-1]["id"]

    assert r.status_code == 201
    assert carts[-1] == test_carts[0]

#delete_menu_item_from_cart Tests

def test_deleting_menu_item_from_cart_success(test_carts, test_users,
                                              cart_test_client, temp_cart_path):
    """Testing a successful deleting of a menu item from a users cart"""

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/" + test_carts[0]["id"]
    request = request + "/" + test_carts[0]["cart_items"][0]["item"]["id"]
    r = cart_test_client.delete(request, headers={"user-id": test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    test_carts[0]["cart_items"] = []

    assert r.status_code == 204
    assert test_carts == carts

def test_deleting_menu_item_from_nonexistent_cart(test_carts, test_users,
                                                  cart_test_client, temp_cart_path):
    """Testing a successful deleting of a menu item from a users cart"""

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/fake-id"
    request = request + "/018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01"
    r = cart_test_client.delete(request, headers= {"user-id" : test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    assert r.status_code == 404
    assert test_carts == carts

def test_deleting_nonexistent_menu_item_from_cart(test_carts, test_users,
                                                  cart_test_client, temp_cart_path):
    """Testing a successful deleting of a menu item from a users cart"""

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/" + test_carts[0]["id"]
    request = request + "/fake-id"
    r = cart_test_client.delete(request, headers= {"user-id" : test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    assert r.status_code == 404
    assert test_carts == carts

def test_add_menu_item_to_cart_integration(test_carts, test_users,
                                           cart_test_client, temp_cart_path ,
                                           menu_item_payload):
    """
    Spec: If a valid cart exists, a user should be able to add a menu item to it.
    Input: valid restaurant_id, valid cart_id, and menu item payload.
    Expected behavior: API returns 201 and the item is added to the cart.
    """

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/" + test_carts[0]["id"]

    r = cart_test_client.post(request, json=menu_item_payload,
                              headers= {"user-id" : test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    assert r.status_code == 201
    assert len(carts[0]["cart_items"]) == 2
    assert carts[0]["cart_items"][1]["item"]["id"] == menu_item_payload["id"]

def test_add_menu_item_to_nonexistent_cart_integration(test_carts, test_users,
                                                       cart_test_client, temp_cart_path,
                                                       menu_item_payload):
    """
    Spec: System should not allow adding items to a cart that does not exist.
    Input: valid restaurant_id but invalid cart_id ("fake-id").
    Expected behavior: API returns 404 and cart data remains unchanged.
    """

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/fake-id"

    r = cart_test_client.post(request, json=menu_item_payload,
                              headers= {"user-id" : test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    assert r.status_code == 404
    assert carts == test_carts
