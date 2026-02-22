"""Integration Tests"""
#pylint: disable=import-error
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.user_repo import UserRepo
from app.routers.user import create_user_repo

client = TestClient(app)

def test_create_user(tmp_path):
    """Integration test of add user functionality"""
    test_user_data_path = tmp_path / "users.json"

    def oveerride_create_user_repo():
        return UserRepo(test_user_data_path)

    app.dependency_overrides[create_user_repo] = oveerride_create_user_repo

    payload ={"name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}

    r = client.post("/users", json=payload)

    data = r.json()
    payload = {"id" : data["id"]} | payload

    assert r.status_code == 201
    assert payload == data
