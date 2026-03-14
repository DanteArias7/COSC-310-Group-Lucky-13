"""Integration tests for restaurant endpoints."""
from datetime import date, time
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
#pylint: disable=too-many-arguments
#pylint: disable=too-many-positional-arguments

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
                "price": 12.99, "tags": ["vegan"], "status" : "Available"
                }]
        }]
@pytest.fixture
def test_restaurant_results(test_restaurants):
    """Initialize Test RestaurantResult data"""
    today = date.today().strftime("%A")
    return [{
            "id": test_restaurants[0]["id"],
            "name": test_restaurants[0]["name"],
            "address": test_restaurants[0]["address"],
            "todays_hours": test_restaurants[0]["hours"][today],
            "tags": test_restaurants[0]["tags"]
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
                "delivery_fee" : 0.35,
                "tax" : 1.30,
                "total": 14.64}]

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

#browse_restaurants Integration Tests

def test_browse_restaurants_integration_without_search_success(mocker, restaurant_test_client,
                                                                test_users,
                                                                test_restaurant_results):
    """Spec: Test retrieving all restaurants via GET /restaurants/browse.
    Input: None
    Expected Behaviour: A List of RestauntResult objects is returned"""

    mocked_time = mocker.patch("app.services.restaurant_services.datetime")
    mocked_time.now.return_value.time.return_value = time(10,30)

    response = restaurant_test_client.get("/restaurants/browse",
                                          headers={"user-id": test_users[1]["id"]})

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    restaurant = data[0]

    assert test_restaurant_results[0] == data[0]

    assert isinstance(restaurant["todays_hours"], str)
    assert isinstance(restaurant["tags"], list)

def test_browse_restaurants_integration_filters_closed_restaurants_open(mocker,
                                                                restaurant_test_client,
                                                                test_users,
                                                                test_restaurant_results):
    """Spec: Test retrieving all restaurants via GET /restaurants/browse.
    Input: None
    Expected Behaviour: A List of RestauntResult objects is returned"""

    mocked_time = mocker.patch("app.services.restaurant_services.datetime")
    mocked_time.now.return_value.time.return_value = time(10,30)

    response = restaurant_test_client.get("/restaurants/browse",
                                          headers={"user-id": test_users[1]["id"]})

    assert response.status_code == 200
    data = response.json()

    assert test_restaurant_results[0] == data[0]

def test_browse_restaurants_integration_filters_closed_restaurants_closed(mocker,
                                                                restaurant_test_client,
                                                                test_users):
    """Spec: Test retrieving all restaurants via GET /restaurants/browse.
    Input: None
    Expected Behaviour: A List of RestauntResult objects is returned"""

    mocked_time = mocker.patch("app.services.restaurant_services.datetime")
    mocked_time.now.return_value.time.return_value = time(18,30)

    response = restaurant_test_client.get("/restaurants/browse",
                                          headers={"user-id": test_users[1]["id"]})

    assert response.status_code == 200
    data = response.json()

    assert data == []

def test_browse_restaurants_with_name_search_success(restaurant_test_client,
                                                    test_restaurant_results,
                                                    test_users):
    """Spec: A user using a search term to find a restaurant should be shown
    restaurants matching, or partially matching the restaurants name.
    Input: A search term that matches or partially matches a restaurant's name
    Expected Behaviour: A List of RestauntResult objects is returned that matches the search term"""

    response = restaurant_test_client.get("/restaurants/browse?search=veg",
                                          headers={"user-id": test_users[1]["id"]})


    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    restaurant = data[0]

    assert test_restaurant_results[0] == data[0]

    assert isinstance(restaurant["todays_hours"], str)
    assert isinstance(restaurant["tags"], list)

def test_browse_restaurants_with_name_and_tags_success(restaurant_test_client,
                                                    test_users,
                                                    test_restaurant_results):
    """Spec: A user using a searched term and specified tags via GET /restaurants/browse, should
    see those specified restaurants.
    Input: A search term that matches a restaurant's name and
    list of tags that matches the restaurants tags.
    Expected Behaviour: A List of RestauntResult objects is
    returned that match the search and tags"""

    response = restaurant_test_client.get("/restaurants/browse?search=veg&tags=vegan",
                                          headers={"user-id": test_users[1]["id"]})

    assert response.status_code == 200
    data = response.json()

    assert test_restaurant_results[0] == data[0]

def test_browse_restaurants_with_not_all_tags(restaurant_test_client,
                                                    test_users):
    """Spec: A user using specified tags of which one matches a restaurant but the other does not,
    should show no matching restaurants.
    Input: A list of tags that includes tags the test restaurant does and does not have.
    Expected Behaviour: An empty list should be returned"""

    response = restaurant_test_client.get("/restaurants/browse?search=veg&tags=vegan&tags=tag",
                                          headers={"user-id": test_users[1]["id"]})

    assert response.status_code == 200
    data = response.json()

    assert data == []


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

#browse_menu_item Integration Tests

def test_browse_menu_items_success(test_restaurants, test_users,
                                            restaurant_test_client, temp_restaurant_path):
    """Spec: If a restaurant has menu items matching the search, it should be returned
    Input:A valid request with a search term that matches a menu item
    Exepected Behaviour:A List of menuitems whose names include the search term is returned"""

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + "/menu?search=veg"
    response = restaurant_test_client.get(request, headers={"user-id": test_users[0]["id"]})

    data = response.json()

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert response.status_code == 200
    assert restaurants[0]["menu"][0] == data[0]

def test_browse_menu_items_no_search_match(test_restaurants, test_users,
                                            restaurant_test_client):
    """Spec: If a restaurant has no menu items matching the search, an empty list should be returned
    Input:A valid request with a search term that does not match a menu item
    Exepected Behaviour:An empty list is returned"""

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + "/menu?search=qqq"
    response = restaurant_test_client.get(request, headers={"user-id": test_users[0]["id"]})

    data = response.json()


    assert response.status_code == 200
    assert data == []

def test_browse_menu_items_with_menu_items_in_price_ranges(test_restaurants, test_users,
                                            restaurant_test_client, temp_restaurant_path):
    """Spec: A valid restaurant has menu items within a price range
    Input:A valid request with a max and min that a menu items price falls between
    Exepected Behaviour:A List of menuitems whose prices are in between max and min,
    with a 200 status"""

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + "/menu?price-max=14.00"
    max_response = restaurant_test_client.get(request, headers={"user-id": test_users[0]["id"]})

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + "/menu?price_min=6.00"
    min_response = restaurant_test_client.get(request, headers={"user-id": test_users[0]["id"]})

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + \
    "/menu?price-max=21.00&price_min=6.00"

    max_and_min_response = restaurant_test_client.get(request,
                                                      headers={"user-id": test_users[0]["id"]})

    max_data = max_response.json()
    min_data = min_response.json()
    min_max_data = max_and_min_response.json()

    with open(temp_restaurant_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert max_response.status_code == 200
    assert restaurants[0]["menu"][0] == max_data[0]
    assert restaurants[0]["menu"][0] == min_data[0]
    assert restaurants[0]["menu"][0] == min_max_data[0]

def test_browse_menu_items_with_menu_items_not_in_price_ranges(test_restaurants, test_users,
                                            restaurant_test_client):
    """Spec: A valid restaurant has menu items not within a price range
    Input:A valid request with a max and min that no menu items price falls between
    Exepected Behaviour:An empty list is returned with a 200 status"""

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + "/menu?price_max=5.00"
    max_response = restaurant_test_client.get(request, headers={"user-id": test_users[0]["id"]})

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + "/menu?price_min=18.00"
    min_response = restaurant_test_client.get(request, headers={"user-id": test_users[0]["id"]})

    request = "/restaurants/" + str(test_restaurants[0]["id"]) + \
        "/menu?price-max=21.00&price_min=18.00"

    max_and_min_response = restaurant_test_client.get(request,
                                                      headers={"user-id": test_users[0]["id"]})

    max_data = max_response.json()
    min_data = min_response.json()
    min_max_data = max_and_min_response.json()

    assert max_response.status_code == 200
    assert max_data == []
    assert min_data == []
    assert min_max_data == []

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
    test_carts[0]["delivery_fee"] = 0.00
    test_carts[0]["total"] = 0.00

    test_carts[0]["id"] = carts[-1]["id"]

    assert r.status_code == 201
    assert carts[-1] == test_carts[0]

#delete_cart_item_from_cart Tests

def test_deleting_cart_item_from_cart_success(test_carts, test_users,
                                              cart_test_client, temp_cart_path,
                                              mocker):
    """Testing a successful deleting of a CartItem from a users cart"""
    distance_mock = mocker.patch("app.routers.restaurant.random.uniform")
    distance_mock.return_value = 1.0

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/" + test_carts[0]["id"]
    request = request + "/" + test_carts[0]["cart_items"][0]["item"]["id"]
    r = cart_test_client.delete(request, headers={"user-id": test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    test_carts[0]["cart_items"] = []

    assert r.status_code == 204
    assert test_carts == carts

def test_deleting_cart_item_from_nonexistent_cart(test_carts, test_users,
                                                  cart_test_client, temp_cart_path):
    """Testing a successful deleting of a CartItem from a users cart"""

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/fake-id"
    request = request + "/018f8c10-7b2a-7f21-9a3c-0a1b2c3d4e01"
    r = cart_test_client.delete(request, headers= {"user-id" : test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    assert r.status_code == 404
    assert test_carts == carts

def test_deleting_nonexistent_cart_item_from_cart(test_carts, test_users,
                                                  cart_test_client, temp_cart_path):
    """Testing a successful deleting of a CartItem from a users cart"""

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/" + test_carts[0]["id"]
    request = request + "/fake-id"
    r = cart_test_client.delete(request, headers= {"user-id" : test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    assert r.status_code == 404
    assert test_carts == carts

#add_cart_item_to_cart Tests

def test_add_cart_item_to_cart_success(test_carts, test_users,
                                           cart_test_client, temp_cart_path ,
                                           menu_item_payload, mocker):
    """
    Spec: If a valid cart exists, a user should be able to add a menu item to it.
    Input: valid restaurant_id, valid cart_id, and menu item payload.
    Expected behavior: API returns 201 and the item is added to the cart.
    """
    distance_mock = mocker.patch("app.routers.restaurant.random.uniform")
    distance_mock.return_value = 1.0

    request = "/restaurants/" + str(test_carts[0]["restaurant_id"])
    request = request + "/cart/" + test_carts[0]["id"]

    r = cart_test_client.post(request, json=menu_item_payload,
                              headers= {"user-id" : test_users[0]["id"]})

    with open(temp_cart_path, "r", encoding="utf-8") as f:
        carts = json.load(f)

    data = r.json()
    assert r.status_code == 201
    assert len(carts[0]["cart_items"]) == 2
    assert carts[0]["cart_items"][1]["item"]["id"] == menu_item_payload["id"]
    assert data["subtotal"]     == 17.99
    assert data["delivery_fee"] == 0.35
    assert data["tax"]          == 1.80
    assert data["total"]        == 20.14

def test_add_cart_item_to_nonexistent_cart_integration(test_carts, test_users,
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
