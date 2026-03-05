"""Tests for restaurant functionality."""
from fastapi import HTTPException
import pytest
from app.schemas.menu import CreateMenuItem, MenuItem, UpdateMenuItem
from app.schemas.restaurant import Restaurant, RestaurantCreate, UpdateRestaurant
from app.services.restaurant_services import RestaurantServices

#pylint: disable=duplicate-code
#pylint: disable=redefined-outer-name
@pytest.fixture
def test_restaurants():
    """Test restaurant data"""
    return [{"id": 101, "name": "Veggie Palace",
                "hours": {"Monday": "9:00-17:00"}, "phone_number": "1234567890",
                "address": "123 Green Street",
                "tags": ["vegan", "brunch"],
                "menu": [{"id": "00000000-0000-0000-0000-0000000000001",
                "name": "Vegan Burger", "description": "Plant-based patty with lettuce and tomato",
                "price": 12.99, "tags": ["vegan"]
                }]
        }]
test_carts = [{"id" : "00000000-0000-0000-0000-000000000001",
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
def mocked_repo(mocker):
    """Creates a mocked repo object for each test"""
    return mocker.Mock()

@pytest.fixture
def restaurant_service(mocked_repo):
    """Creates a restaurant service object with mocked repo"""
    return RestaurantServices(mocked_repo)

#fetch_all_restaurants Tests

def test_fetch_all_restaurants(test_restaurants, mocked_repo, restaurant_service):
    """Testing that fetch_all_restaurants returns a list of restaurants"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    result = restaurant_service.fetch_all_restaurants()

    assert result == test_restaurants

#fetch_restaurant Tests

def test_fetch_restaurant_success(test_restaurants, mocked_repo, restaurant_service):
    """Testing that fetch_restaurant returns the result when requested ID exists"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    result = restaurant_service.fetch_restaurant(101)
    result = result.model_dump()

    assert result == test_restaurants[0]


def test_fetch_restaurant_not_found(mocked_repo, restaurant_service):
    """Testing that fetch_restaurant raises HTTPException when ID does not exist"""

    mocked_repo.load_all_restaurants.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.fetch_restaurant("non-existent-id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Restaurant not found"

#create_restaurant  Unit Tests
def test_create_new_restaurant(mocker, mocked_repo, restaurant_service):
    """Scenario: check that creating a valid restaurant returns a valid restaurant"""
    mocked_id = 99
    id_mock = mocker.patch("app.services.restaurant_services.random.randint")
    id_mock.return_value = mocked_id

    mocked_repo.load_all_restaurants.return_value = []

    payload = RestaurantCreate(
        name="Taco Town",
        hours={"Monday": "10:00-20:00"},
        phone_number="5555555555",
        address="123 Taco Lane",
        tags=["mexican"],
        menu=[
            MenuItem(
                id="00000000-0000-0000-0000-000000000011",
                name="Taco",
                description="Beef taco",
                price=5.0,
                tags=["mexican","beef"]
            )
        ]
    )

    result = restaurant_service.create_new_restaurant(payload)

    assert result.id == mocked_id
    assert result.name == "Taco Town"
    assert result.hours == {"Monday": "10:00-20:00"}
    assert result.phone_number == "5555555555"
    assert result.address == "123 Taco Lane"
    assert result.tags == ["mexican"]
    assert result.menu[0].name == "Taco"
    mocked_repo.save_all_restaurants.assert_called_once()

#update_restaurant Unit Tests

def test_update_restaurant_success(test_restaurants, mocked_repo, restaurant_service):
    """Test that the update_restaurant returns the proper restaurant object"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    payload = UpdateRestaurant(name = "Meat Palace",
                            hours= {"Monday": "9:00-2:00"},
                            phone_number="9876543210",
                            address="321  Street",
                            tags=["brunch"])

    expected_restaurant =  Restaurant(id=101,
                                    name = "Meat Palace",
                                    hours= {"Monday": "9:00-2:00"},
                                    phone_number="9876543210",
                                    address="321  Street",
                                    tags=["brunch"],
                                    menu=[{"id": "00000000-0000-0000-0000-0000000000001",
                                    "name": "Vegan Burger",
                                    "description": "Plant-based patty with lettuce and tomato",
                                    "price": 12.99, "tags": ["vegan"]
                                    }])

    updated_restaurant = restaurant_service.update_restaurant(
                            test_restaurants[0]["id"], payload)

    assert updated_restaurant == expected_restaurant

def test_update_nonexistent_restaurant(test_restaurants, mocked_repo, restaurant_service):
    """Test that the update_menu_item returns the proper menu item object"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    payload = UpdateRestaurant(name = "Meat Palace",
                            hours= {"Monday": "9:00-2:00"},
                            phone_number="9876543210",
                            address="321  Street",
                            tags=["brunch"])

    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.update_restaurant(102,
                                             payload)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Restaurant 102 Not Found"

#delete_restaurant Unit Tests

def test_delete_nonexistent_restaurant(test_restaurants, mocked_repo, restaurant_service):
    """Test that delete_restaurant raises an exception if the restaurant id is not found"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.delete_restaurant(
            "999")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Restaurant 999 Not Found"

#add_menu_item Unit Tests

def test_add_menu_item(mocker, test_restaurants, mocked_repo, restaurant_service):
    """Test that adding a menu item returns the proper menu item"""
    mocked_uuid = '00000000-0000-0000-0000-000000000002'
    uuid_mock = mocker.patch("app.services.restaurant_services.uuid.uuid7")
    uuid_mock.return_value = mocked_uuid

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    payload = CreateMenuItem(name="Classic Burger", description="Cheeseburger",
                             price= 10.50, tags=["burger"])

    expected_menu_item = MenuItem(id=mocked_uuid,name="Classic Burger", description="Cheeseburger",
                                  price= 10.50, tags=["burger"])

    new_menu_item = restaurant_service.add_item_to_menu(test_restaurants[0]["id"], payload)

    assert new_menu_item == expected_menu_item

#update_menu_item Unit Tests

def test_update_menu_item_success(test_restaurants, mocked_repo, restaurant_service):
    """Test that the update_menu_item returns the proper menu item object"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    payload = UpdateMenuItem(name="Classic Burger", description="Cheeseburger",
                             price= 10.50, tags=["burger"])

    expected_menu_item = MenuItem(id="00000000-0000-0000-0000-0000000000001",
                                  name="Classic Burger", description="Cheeseburger",
                                  price= 10.50, tags=["burger"])

    updated_menu_item = restaurant_service.update_menu_item(
                            test_restaurants[0]["id"],
                            "00000000-0000-0000-0000-0000000000001", payload)

    assert updated_menu_item == expected_menu_item

def test_update_menu_item_nonexistent_menu_item(test_restaurants, mocked_repo,
                                                restaurant_service):
    """Test that update menu item method returns proper exception if menuitem does not exist"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    payload = UpdateMenuItem(name="Classic Burger", description="Cheeseburger",
                             price= 10.50, tags=["burger"])

    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.update_menu_item(test_restaurants[0]["id"],
                                             "00000000-0000-0000-0000-0000000000002", payload)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Menu Item 00000000-0000-0000-0000-0000000000002 Not Found"

def test_update_menu_item_nonexistent_restaurant(test_restaurants, mocked_repo,
                                                restaurant_service):
    """Test that update menu item method returns proper exception if restaurant does not exist"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    payload = UpdateMenuItem(name="Classic Burger", description="Cheeseburger",
                             price= 10.50, tags=["burger"])

    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.update_menu_item("00000000-0000-0000-0000-0000000000002",
                                             "00000000-0000-0000-0000-0000000000001", payload)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Restaurant 00000000-0000-0000-0000-0000000000002 Not Found"

#delete_menu_item Unit Tests

def test_delete_last_menu_item(test_restaurants, mocked_repo, restaurant_service):
    """Test that delete_menu_item does not delete the last menu item of the restaurant"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.delete_menu_item(
            101, "00000000-0000-0000-0000-0000000000001")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Restaurant must have at least one menu item."
