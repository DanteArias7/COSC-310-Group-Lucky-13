"""Integration Tests for users"""
#pylint: disable=import-error
import json
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.repositories.user_repo import UserRepo
from app.routers.user import create_user_repo

client = TestClient(app)


def test_get_user_successful(tmp_path):
    """Scenario: A valid user attempts to get their own profile
    Input: A request including a header with a valid id
    Expected Behaviour: Matching user object is returned"""
    test_user_data_path = tmp_path / "users.json"

    def override_create_user_repo():
        return UserRepo(test_user_data_path)

    app.dependency_overrides[create_user_repo] = override_create_user_repo

    user = [{"id" : "00000000-0000-0000-0000-000000000001", "name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}]

    with open(test_user_data_path, "w", encoding="utf-8") as f:
        json.dump(user, f, ensure_ascii=False)

    request = "/users/00000000-0000-0000-0000-000000000001"

    r = client.get(request, headers={"user-id": "00000000-0000-0000-0000-000000000001"})

    assert r.status_code == 200
    assert r.json() == user[0]

def test_get_nonexistent_user(tmp_path):
    """Scenario: A valid user attempts to get their own profile
    Input: A request including a header with a valid id
    Expected Behaviour: Matching user object is returned"""
    test_user_data_path = tmp_path / "users.json"

    def override_create_user_repo():
        return UserRepo(test_user_data_path)

    app.dependency_overrides[create_user_repo] = override_create_user_repo

    user = [{"id" : "00000000-0000-0000-0000-000000000001", "name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}]

    with open(test_user_data_path, "w", encoding="utf-8") as f:
        json.dump(user, f, ensure_ascii=False)

    request = "/users/00000000-0000-0000-0000-000000000002"

    r = client.get(request, headers={"user-id": "00000000-0000-0000-0000-000000000002"})

    assert r.status_code == 404
    assert r.json() == {"detail" : "User '00000000-0000-0000-0000-000000000002' not found."}


def test_create_user(tmp_path):
    """Integration test of add user functionality"""
    test_user_data_path = tmp_path / "users.json"

    def override_create_user_repo():
        return UserRepo(test_user_data_path)

    app.dependency_overrides[create_user_repo] = override_create_user_repo

    payload = {"name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}

    r = client.post("/users", json=payload)

    data = r.json()
    payload = {"id" : data["id"]} | payload

    assert r.status_code == 201
    assert payload == data

def test_update_user_success(tmp_path):
    """Integration test of update user functionality with proper input"""
    test_user_data_path = tmp_path / "users.json"

    def override_update_user_repo():
        return UserRepo(test_user_data_path)

    app.dependency_overrides[create_user_repo] = override_update_user_repo


    initial_user = [{"id" : "1", "name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}]

    with open(test_user_data_path, "w", encoding="utf-8") as f:
        json.dump(initial_user, f, ensure_ascii=False)

    payload = {"name" : "Jeff", "email" : "Jeffsmith@gmail.com",
                "phone_number" : "555-555-5555", "address" : "321 Ellis Rd, Kelowna, BC, A1B2C3",
                "password" : "pass",  "role" : "customer"}

    r = client.put("/users/1", headers={"user-id" : "1"}, json=payload)
    data = r.json()
    payload = {"id" : "1"} | payload

    assert r.status_code == 200
    assert payload == data

def test_update_user_unsuccessful(tmp_path):
    """Integration test of update user functionality when user does not exist"""
    test_user_data_path = tmp_path / "users.json"

    def override_update_user_repo():
        return UserRepo(test_user_data_path)

    app.dependency_overrides[create_user_repo] = override_update_user_repo

    initial_user = [{"id" : "2", "name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}]

    with open(test_user_data_path, "w", encoding="utf-8") as f:
        json.dump(initial_user, f, ensure_ascii=False)

    payload = {"name" : "Jeff", "email" : "Jeffsmith@gmail.com",
                "phone_number" : "555-555-5555", "address" : "321 Ellis Rd, Kelowna, BC, A1B2C3",
                "password" : "pass",  "role" : "customer"}

    r = client.put("/users/1", headers={"user-id" : "1"}, json=payload)
    data = r.json()
    payload = {"id" : "1"} | payload

    assert r.status_code == 404
    assert not payload == data

def test_delete_user_success(tmp_path):
    """Integration test of delete user functionality when user does exist"""
    test_user_data_path = tmp_path / "users.json"

    def override_delete_user_repo():
        return UserRepo(test_user_data_path)

    app.dependency_overrides[create_user_repo] = override_delete_user_repo

    initial_user = [{"id" : "1", "name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}]

    with open(test_user_data_path, "w", encoding="utf-8") as f:
        json.dump(initial_user, f, ensure_ascii=False)

    r = client.delete("/users/1", headers={"user-id" : "1"})

    with open(test_user_data_path, "r", encoding="utf-8") as f:
        users = json.load(f)

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert users == []

def test_delete_user_unsuccessful(tmp_path):
    """Integration test of delete user functionality when user does exist"""
    test_user_data_path = tmp_path / "users.json"

    def override_delete_user_repo():
        return UserRepo(test_user_data_path)

    app.dependency_overrides[create_user_repo] = override_delete_user_repo

    initial_user = [{"id" : "1", "name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}]

    with open(test_user_data_path, "w", encoding="utf-8") as f:
        json.dump(initial_user, f, ensure_ascii=False)

    r = client.delete("/users/2", headers={"user-id" : "2"})

    with open(test_user_data_path, "r", encoding="utf-8") as f:
        users = json.load(f)

    assert r.status_code == 404
    assert users == initial_user
