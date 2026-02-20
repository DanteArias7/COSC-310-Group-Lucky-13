"""Integration Tests"""
#pylint: disable=import-error
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    """Integration test of add user functionality"""
    payload ={"name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}

    r = client.post("/users", json=payload)
    data = r.json()
    payload = {"id" : data["id"], "name" : "Alex", "email" : "alexsmith@gmail.com",
                "phone_number" : "123-456-7890", "address" : "123 Baron Rd, Kelowna, BC, A1B2C3",
                "password" : "password",  "role" : "customer"}

    assert r.status_code == 201
    assert payload == data
