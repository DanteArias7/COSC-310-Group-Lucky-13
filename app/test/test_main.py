"""Integration Tests for users"""
#pylint: disable=import-error
import json

from fastapi.testclient import TestClient
from app.main import app
from app.repositories.user_repo import UserRepo
from app.routers.user import create_user_repo

client = TestClient(app)

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

    r = client.put("/users/1", json=payload)
    data = r.json()
    payload = {"id" : "1"} | payload

    assert r.status_code == 200
    assert payload == data

def test_update_user_unsuccessfuk(tmp_path):
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

    r = client.put("/users/1", json=payload)
    data = r.json()
    payload = {"id" : "1"} | payload

    assert r.status_code == 404
    assert not payload == data