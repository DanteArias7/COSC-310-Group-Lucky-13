"""Tests for restaurant functionality."""
from datetime import date

from fastapi import HTTPException
import pytest
from app.schemas.menu import CreateMenuItem, MenuItem, UpdateMenuItem
from app.schemas.restaurant import Restaurant, RestaurantCreate, RestaurantResult, UpdateRestaurant
from app.services.restaurant_services import RestaurantServices

#pylint: disable=duplicate-code
#pylint: disable=redefined-outer-name
@pytest.fixture
def test_restaurants():
    """Test restaurant data"""
    return [{"id": 101,
              "user_id": "00000000-0000-0000-0000-000000000001",
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
def test_restaurant_results(test_restaurants):
    """Initialize Test RestaurantResult data"""
    return [RestaurantResult(id=test_restaurants[0]["id"],
                                name=test_restaurants[0]["name"],
                                address=test_restaurants[0]["address"],
                                todays_hours=test_restaurants[0]["hours"]["Monday"],
                                tags=test_restaurants[0]["tags"])]

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
    result[0] = result[0].model_dump()

    today = date.today().strftime("%A")

    assert test_restaurants[0]["id"] == result[0]["id"]
    assert test_restaurants[0]["name"] == result[0]["name"]
    assert test_restaurants[0]["address"] == result[0]["address"]
    assert test_restaurants[0]["hours"][today] == result[0]["todays_hours"]
    assert test_restaurants[0]["tags"] == result[0]["tags"]

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

#fetch_name_searched_restaurants Tests
def test_fetch_name_searched_restaurant_success(test_restaurants, mocked_repo, restaurant_service):
    """Testing that fetch_restaurant returns the result when requested ID exists"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    result = restaurant_service.fetch_name_searched_restaurants("veg")
    result[0] = result[0].model_dump()

    today = date.today().strftime("%A")

    assert test_restaurants[0]["id"] == result[0]["id"]
    assert test_restaurants[0]["name"] == result[0]["name"]
    assert test_restaurants[0]["address"] == result[0]["address"]
    assert test_restaurants[0]["hours"][today] == result[0]["todays_hours"]
    assert test_restaurants[0]["tags"] == result[0]["tags"]

def test_fetch_name_searched_restaurant_no_matching_restaurant(test_restaurants,
                                                               mocked_repo, restaurant_service):
    """Testing that fetch_restaurant returns the result when requested ID exists"""

    mocked_repo.load_all_restaurants.return_value = test_restaurants

    result = restaurant_service.fetch_name_searched_restaurants("qqq")

    assert result == []

#create_restaurant  Unit Tests
def test_create_new_restaurant(mocker, mocked_repo, restaurant_service):
    """Scenario: check that creating a valid restaurant returns a valid restaurant"""
    mocked_id = 99
    id_mock = mocker.patch("app.services.restaurant_services.random.randint")
    id_mock.return_value = mocked_id

    mocked_repo.load_all_restaurants.return_value = []

    user_id= "00000000-0000-0000-0000-000000000001"

    payload = RestaurantCreate(
        name="Taco Town",
        user_id=user_id,
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

    result = restaurant_service.create_new_restaurant(user_id, payload)

    assert result.id == mocked_id
    assert result.user_id == "00000000-0000-0000-0000-000000000001"
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
                                    user_id= "00000000-0000-0000-0000-000000000001",
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

#filter_restaurants_by_tags Unit Tests
def test_filter_restaurant_by_tags_success(restaurant_service, test_restaurant_results):
    """Spec: A list of tags is given, matching at least one restaurant
    Input: A list of RestaurantResults and a List of tags matching a restaurants tags,
    Expected Behaviour: Method retruns a List of RestaurantResult objects,
    whose tags include all the given tags"""

    result = restaurant_service.filter_restaurants_by_tags(test_restaurant_results, ["vegan"])

    assert result == test_restaurant_results

def test_filter_restaurant_by_tags_not_all_tags(restaurant_service, test_restaurant_results):
    """Spec: If none of the restaurants contain all the tags specified, nothing should be returned
    Input: A valid list of RestaurantResults and a list of tags that do not match any restaurant
    Expected Behaviour: Method returnns an empty list"""

    result = restaurant_service.filter_restaurants_by_tags(test_restaurant_results,
                                                           ["vegan", "green"])

    assert result == []

#fetch_name_searched_menu_items Unit Tests
def test_fetch_name_searched_menu_items_success(test_restaurants, restaurant_service):
    """Spec: A restaurant exists and has menu items matching the search term,
    they should be returned in a list
    Input: A valid restaurant and a search term matching a menu item,
    Expected Behaviour: Method retruns a List of MenuItem objects"""

    payload = Restaurant(**test_restaurants[0])

    expected_menu_item = test_restaurants[0]["menu"][0]

    result = restaurant_service.get_name_searched_menu_items(payload, "veg")

    assert result[0].model_dump() == expected_menu_item

def test_fetch_name_searched_menu_items_no_search_match(test_restaurants, restaurant_service):
    """Spec: A restaurant exists and does not have a menu item matching the search term,
    it should return nothing
    Input: A valid restaurant and a search term not matching a menu item,
    Expected Behaviour: Method retruns an empty list"""

    payload = Restaurant(**test_restaurants[0])

    result = restaurant_service.get_name_searched_menu_items(payload, "qqq")

    assert result == []

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
