"""Unit tests for favorite services."""
from fastapi import HTTPException
import pytest

from app.schemas.favorite import Favorite
from app.services.favorite_services import FavoriteServices

#pylint: disable=redefined-outer-name


@pytest.fixture
def favorite_payload():
    """Favorite Payload"""
    return Favorite(
        id = "00000000-0000-0000-0000-000000000001",
        user_id="00000000-0000-0000-0000-000000000001",
        restaurant_id=101,
        menu_item_id="m1"
    )

@pytest.fixture
def favorite_payload_delete():
    """Favorite Payload for delete test"""
    return {
        "id": "fav2",
        "user_id": "00000000-0000-0000-0000-000000000002",
        "restaurant_id": 101,
        "menu_item_id": "m1"
    }

@pytest.fixture
def favorites_data():
    """Favorite data for testing"""
    return [
        {
            "id": "fav1",
            "user_id": "00000000-0000-0000-0000-000000000001",
            "restaurant_id": 101,
            "menu_item_id": "m1"
        },
        {
            "id": "fav2",
            "user_id": "00000000-0000-0000-0000-000000000001",
            "restaurant_id": 102,
            "menu_item_id": "m2"
        }
    ]

@pytest.fixture
def test_user_id():
    """User ID for tests"""
    return "00000000-0000-0000-0000-000000000001"

@pytest.fixture
def mocked_repo(mocker):
    """Create mocked repo object for each test"""
    mocked_repo = mocker.Mock()
    return mocked_repo

@pytest.fixture
def mock_restaurant_service(mocker):
    """Create mocked restaurant service for each test"""
    service = mocker.Mock()

    restaurant = mocker.Mock()
    restaurant.menu = [mocker.Mock(id="m1")]

    service.fetch_restaurant.return_value = restaurant

    return service

@pytest.fixture
def favorite_service(mocked_repo, mock_restaurant_service):
    """Creates favorite service with mocked dependencies"""
    return FavoriteServices(
        mocked_repo,
        mock_restaurant_service
    )

def test_add_favorite_success(favorite_service, mocked_repo, favorite_payload):
    """
    Spec: Adding a valid favorite should succeed
    Input: valid restaurant id and menu item id.
    Expected behavior: Favorite is added successfully and returned.
    """

    mocked_repo.load_all_favorites.return_value = []

    result = favorite_service.add_favorite(favorite_payload)

    assert result["menu_item_id"] == "m1"
    mocked_repo.save_all_favorites.assert_called_once()

def test_add_favorite_item_not_first_in_menu(favorite_service, mocked_repo,
                                             favorite_payload, mocker):
    """
    Spec: Adding a menu item that is not the first in the menu should succeed
    Input: valid restaurant id and menu item id that is not the first in the menu.
    Expected behavior: Favorite is added successfully and returned.
    """
    mocked_repo.load_all_favorites.return_value = []

    restaurant = mocker.Mock()
    restaurant.menu = [mocker.Mock(id="different-id"), mocker.Mock(id="m1")]
    favorite_service.restaurant_service.fetch_restaurant.return_value = restaurant

    result = favorite_service.add_favorite(favorite_payload)

    assert result["menu_item_id"] == "m1"
    mocked_repo.save_all_favorites.assert_called_once()


def test_add_favorite_invalid_menu_item(favorite_service, mocked_repo, favorite_payload, mocker):
    """
    Spec: Invalid menu item should raise 404
    Input: valid restaurant id and invalid menu item id.
    Expected behavior: HTTPException with status code 404 is raised.
    """
    mocked_repo.load_all_favorites.return_value = []

    restaurant = mocker.Mock()
    restaurant.menu = [mocker.Mock(id="different-id")]
    favorite_service.restaurant_service.fetch_restaurant.return_value = restaurant

    with pytest.raises(HTTPException) as exc_info:
        favorite_service.add_favorite(favorite_payload)

    assert exc_info.value.status_code == 404

def test_remove_favorite_success(favorite_service, mocked_repo, favorite_payload_delete):
    """
    Spec: Removing an existing favorite should succeed
    Input: valid favorite id belonging to the user.
    Expected behavior: Favorite is removed and saved.
    """

    mocked_repo.load_all_favorites.return_value = [favorite_payload_delete]

    favorite_service.remove_favorite("fav2",
        "00000000-0000-0000-0000-000000000002")

    mocked_repo.save_all_favorites.assert_called_once()


def test_remove_favorite_unauthorized(favorite_service, mocked_repo, favorite_payload_delete):
    """
    Spec: Removing another user's favorite should raise 403
    Input: valid favorite id but wrong user id.
    Expected behavior: HTTPException with status code 403 is raised.
    """

    mocked_repo.load_all_favorites.return_value = [favorite_payload_delete]

    with pytest.raises(HTTPException) as exc_info:
        favorite_service.remove_favorite("fav2", "wrong-user")

    assert exc_info.value.status_code == 403


def test_remove_favorite_not_found(favorite_service, mocked_repo):
    """
    Spec: Removing a non-existent favorite should raise 404
    Input: invalid favorite id.
    Expected behavior: HTTPException with status code 404 is raised.
    """

    mocked_repo.load_all_favorites.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        favorite_service.remove_favorite("invalid-id", "00000000-0000-0000-0000-000000000002")

    assert exc_info.value.status_code == 404

def test_add_favorite_duplicate(favorite_service, mocked_repo, favorite_payload):
    """
    Spec: Adding a duplicate favorite should raise 400
    Input: valid restaurant id and menu item id that already exists in favorites.
    Expected behavior: HTTPException with status code 400 is raised.
    """

    mocked_repo.load_all_favorites.return_value = [favorite_payload.model_dump()]

    with pytest.raises(HTTPException) as exc_info:
        favorite_service.add_favorite(favorite_payload)

    assert exc_info.value.status_code == 400

def test_get_favorites_by_user_id_success(favorite_service, mocked_repo,
                                          favorites_data, test_user_id):
    """
    Spec: Getting favorites for a user should return their favorites
    Input: valid user id.
    Expected behavior: List of favorites belonging to the user is returned.
    """

    mocked_repo.load_all_favorites.return_value = favorites_data

    result = favorite_service.get_favorites_by_user_id(test_user_id)

    assert len(result) == 2

def test_get_favorites_by_user_id_no_favorites(favorite_service, mocked_repo, test_user_id):
    """
    Spec: Getting favorites for a user with no favorites should return empty list
    Input: valid user id with no favorites.
    Expected behavior: HTTPException with status code 404 is raised.
    """

    mocked_repo.load_all_favorites.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        favorite_service.get_favorites_by_user_id(test_user_id)

    assert exc_info.value.status_code == 404
