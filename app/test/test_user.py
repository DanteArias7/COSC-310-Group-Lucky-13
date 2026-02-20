"""Tests for users"""
#pylint: disable=import-error
from app.schemas.user import User, UserCreate
from app.services.user_services import UserServices

def test_create_user(mocker):
    """Test for creating a user method"""
    mocked_uuid = '00000000-0000-0000-0000-000000000001'
    uuid_mock = mocker.patch("app.services.user_services.uuid.uuid7")
    uuid_mock.return_value = mocked_uuid

    mocked_repo = mocker.Mock()
    user_service = UserServices(mocked_repo)

    payload = UserCreate(name="Alex", email="alexsmith@gmail.com",
                         phone_number="123-456-7890", address="123 Baron Rd, Kelowna, BC, A1B2C3",
                         password="password", role="customer")

    expected_user = User(id='00000000-0000-0000-0000-000000000001', name="Alex",
                         email="alexsmith@gmail.com", phone_number="123-456-7890",
                         address="123 Baron Rd, Kelowna, BC, A1B2C3",
                         password="password", role="customer")

    actual_user = user_service.create_user(payload)

    assert actual_user == expected_user
