"""Unit Tests for users"""
#pylint: disable=import-error
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user_services import UserServices

def test_create_user(mocker):
    """Unit Test for creating a user method"""
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

def test_update_user(mocker):
    """Unit Test for updating a user method"""
    mocked_repo = mocker.Mock()
    user_service = UserServices(mocked_repo)

    mocked_load_all_users = [{"id" : "1", "name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"},
                {"id" : "2", "name" : "Jeff", "email" : "Jeffsmith@gmail.com",
                "phone_number" : "555-555-5555", "address" : "321 Ellis Rd, Kelowna, BC, A1B2C3",
                "password" : "pass",  "role" : "customer"}]

    mocked_repo.load_all_users.return_value = mocked_load_all_users

    payload = UserUpdate(name="Alex", email="alexsmith@gmail.com",
                         phone_number="123-456-7890", address="123 Baron Rd, Kelowna, BC, A1B2C3",
                         password="password", role="customer")

    expected_user = User(id='2', name="Alex",
                         email="alexsmith@gmail.com", phone_number="123-456-7890",
                         address="123 Baron Rd, Kelowna, BC, A1B2C3",
                         password="password", role="customer")

    updated_user = user_service.update_user("2", payload)

    assert updated_user == expected_user
