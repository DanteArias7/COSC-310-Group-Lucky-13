"""Integration tests for restaurant endpoints."""

import json

from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.repositories.restaurant_repo import RestaurantRepo
from app.routers.restaurant import create_restaurant_repo

# pylint: disable=redefined-outer-name
client = TestClient(app)

@pytest.fixture
def test_restaurants():
    """Initialize test restaurant data for each test"""
    return [{"id": "00000000-0000-0000-0000-0000000000001", "name": "Veggie Palace",
                "hours": {"Monday": "9:00-17:00"}, "phone_number": "1234567890",
                "address": "123 Green Street",
                "tags": ["vegan", "brunch"],
                "menu": [{"id": "00000000-0000-0000-0000-0000000000001",
                "name": "Vegan Burger", "description": "Plant-based patty with lettuce and tomato",
                "price": 12.99, "tags": ["vegan"]
                }]
        }]

def test_get_all_restaurants_integration():
    """Test retrieving all restaurants via GET /restaurants/."""
    response = client.get("/restaurants/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    restaurant = data[0]

    assert "id" in restaurant
    assert "name" in restaurant
    assert "phone_number" in restaurant
    assert "address" in restaurant
    assert "hours" in restaurant
    assert "tags" in restaurant
    assert "menu" in restaurant

    assert isinstance(restaurant["hours"], dict)
    assert isinstance(restaurant["tags"], list)
    assert isinstance(restaurant["menu"],list)


def test_get_single_restaurant_integration():
    """Test retrieving a single restaurant via GET /restaurants/{id}."""
    response = client.get("/restaurants/00000000-0000-0000-0000-0000000000001")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == "00000000-0000-0000-0000-0000000000001"
    assert "name" in data
    assert "phone_number" in data
    assert "hours" in data
    assert "tags" in data
    assert "address" in data
    assert "menu" in data

    assert isinstance(data["tags"], list)
    assert isinstance(data["menu"], list)


def test_get_nonexistent_restaurant_integration():
    """Test retrieving a restaurant that does not exist."""
    response = client.get("/restaurants/non-existent-id")

    assert response.status_code == 404

def test_updating_restaurant_successful(tmp_path, test_restaurants):
    """Testing successful updating of a restaurants information"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_restaurant_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_restaurant_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    payload = {"name": "Meat Palace",
                "hours": {"Monday": "9:00-2:00"}, "phone_number": "9876543210",
                "address": "321 Red Street",
                "tags": ["brunch"]}

    r = client.put("/restaurants/00000000-0000-0000-0000-0000000000001", json=payload)


    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    test_restaurants[0]["name"] = "Meat Palace"
    test_restaurants[0]["hours"] = {"Monday" : "9:00-2:00"}
    test_restaurants[0]["phone_number"] = "9876543210"
    test_restaurants[0]["address"] = "321 Red Street"
    test_restaurants[0]["tags"] = ["brunch"]

    assert r.status_code == 200
    assert restaurants == test_restaurants

def test_updating_nonexistent_restaurant(tmp_path, test_restaurants):
    """Testing unsuccesful updating of a resturant that does not exist"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_restaurant_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_restaurant_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    payload = {"name": "Meat Palace",
                "hours": {"Monday": "9:00-2:00"}, "phone_number": "9876543210",
                "address": "321 Red Street",
                "tags": ["brunch"]}

    r = client.put("/restaurants/00000000-0000-0000-0000-0000000000002", json=payload)


    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_delete_restaurant_successful(tmp_path, test_restaurants):
    """Testing successful updating of a restaurants information"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_restaurant_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_restaurant_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    r = client.delete("/restaurants/00000000-0000-0000-0000-0000000000001")


    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 204
    assert restaurants == []

def test_delete_nonexistent_restaurant(tmp_path, test_restaurants):
    """Testing successful updating of a restaurants information"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_restaurant_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_restaurant_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    r = client.delete("/restaurants/00000000-0000-0000-0000-0000000000009")

    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_adding_menu_item(tmp_path, test_restaurants):
    """Testing adding a menu item to a restaurant's menu"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_add_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_add_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    payload = {"name": "Classic Burger",
                "description": "Cheeseburger", "price": 10.50, "tags": ["burger"]}

    r = client.post("/restaurants/00000000-0000-0000-0000-0000000000001/menu", json=payload)

    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    menu_item = r.json()

    test_restaurants[0]["menu"].append(menu_item)

    assert r.status_code == 201
    assert restaurants == test_restaurants

def test_adding_menu_item_already_exists(tmp_path, test_restaurants):
    """Testing adding a menu item that already exists in a restaurant's menu"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_add_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_add_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    payload = {"name": "Vegan Burger",
                "description": "Cheeseburger", "price": 10.50, "tags": ["burger"]}

    r = client.post("/restaurants/00000000-0000-0000-0000-0000000000001/menu", json=payload)

    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 409
    assert restaurants == test_restaurants

def test_adding_menu_item_nonexistent_restaurant(tmp_path, test_restaurants):
    """Testing adding a menu item to a restaurant that does not exist"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_add_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_add_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    payload = {"name": "Vegan Burger",
                "description": "Cheeseburger", "price": 10.50, "tags": ["burger"]}

    r = client.post("/restaurants/00000000-0000-0000-0000-0000000000002/menu", json=payload)

    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_updating_menu_item_successful(tmp_path, test_restaurants):
    """Testing successful updating of a menu item to a menu"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    payload = {"name": "Hot Dog", "description": "Beef hot dog on bun",
                "price": 5.99, "tags": ["beef"]}

    r = client.put("/restaurants/00000000-0000-0000-0000-0000000000001/menu/" \
    "00000000-0000-0000-0000-0000000000001", json=payload)


    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    test_restaurants[0]["menu"][0]["name"] = "Hot Dog"
    test_restaurants[0]["menu"][0]["description"] = "Beef hot dog on bun"
    test_restaurants[0]["menu"][0]["price"] = 5.99
    test_restaurants[0]["menu"][0]["tags"] = ["beef"]

    assert r.status_code == 200
    assert restaurants == test_restaurants

def test_updating_nonexistent_menu_item(tmp_path, test_restaurants):
    """Testing unsuccessful updating of a menu item that does not exist"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    payload = {"name": "Hot Dog", "description": "Beef hot dog on bun",
                "price": 5.99, "tags": ["beef"]}

    r = client.put("/restaurants/00000000-0000-0000-0000-0000000000001/" \
    "menu/00000000-0000-0000-0000-0000000000002", json=payload)


    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_updating_menu_item_to_nonexistent_restaurant(tmp_path, test_restaurants):
    """Testing unsuccessful updating of a menu item to restaurant that does not exist"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    payload = {"name": "Hot Dog", "description": "Beef hot dog on bun",
                "price": 5.99, "tags": ["beef"]}

    r = client.put("/restaurants/00000000-0000-0000-0000-0000000000001/," \
    "menu/00000000-0000-0000-0000-0000000000002", json=payload)


    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_deleting_menu_item_success(tmp_path, test_restaurants):
    """Testing a successful deleting of a menu item"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_delete_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_delete_menu_item_repo

   # Appending a second menu item so deletion is allowed as empty menus are not allowed
    test_restaurants[0]["menu"].append({
        "id": "00000000-0000-0000-0000-0000000000002",
        "name": "Fries",
        "description": "Yam Fries",
        "price": 5.99,
        "tags": ["fries"]
    })

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    r = client.delete("/restaurants/00000000-0000-0000-0000-0000000000001/" \
    "menu/00000000-0000-0000-0000-0000000000001")


    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 204
    assert len(restaurants[0]["menu"]) == 1
    assert restaurants[0]["menu"][0]["id"] == "00000000-0000-0000-0000-0000000000002"

def test_deleting_menu_item_to_nonexistent_restaurant(tmp_path, test_restaurants):
    """Testing unsuccessful deleting of menu item from a restaurant that does not exist"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    r = client.delete("/restaurants/00000000-0000-0000-0000-0000000000002/" \
    "menu/00000000-0000-0000-0000-0000000000001")

    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_deleting_nonexistent_menu_item(tmp_path, test_restaurants):
    """Testing unsuccessful deleting of a menu item that does not exist"""
    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_update_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_update_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    r = client.delete("/restaurants/00000000-0000-0000-0000-0000000000001/" \
    "menu/00000000-0000-0000-0000-0000000000002")

    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 404
    assert restaurants == test_restaurants

def test_deleting_last_menu_item_fails(tmp_path, test_restaurants):
    """Testing unsuccessful deletion of the last remaining menu item"""

    test_restaurant_data_path = tmp_path / "restaurants.json"

    def override_delete_menu_item_repo():
        return RestaurantRepo(test_restaurant_data_path)

    app.dependency_overrides[create_restaurant_repo] = override_delete_menu_item_repo

    with open(test_restaurant_data_path, "w", encoding="utf-8") as f:
        json.dump(test_restaurants, f, ensure_ascii=False)

    r = client.delete(
        "/restaurants/00000000-0000-0000-0000-0000000000001/"
        "menu/00000000-0000-0000-0000-0000000000001"
    )

    with open(test_restaurant_data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    assert r.status_code == 400
    assert restaurants == test_restaurants
