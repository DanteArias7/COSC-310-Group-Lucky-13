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
