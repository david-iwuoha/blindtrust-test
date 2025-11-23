# tests/test_accounts.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)

def get_demo_token():
    # login as demo_user
    resp = client.post("/auth/dev-login", json={"username": "demo_user"})
    data = resp.json()
    return data["token"]

def test_balance():
    token = get_demo_token()
    resp = client.get("/accounts/balance", headers={"Authorization": token})
    assert resp.status_code == 200
    assert "balance" in resp.json()

def test_transfer_success():
    token = get_demo_token()
    # ensure john exists as beneficiary
    resp = client.post("/accounts/transfer", json={"recipient": "john", "amount": 1000}, headers={"Authorization": token})
    assert resp.status_code == 200
    data = resp.json()
    assert "result" in data
    assert "from_balance" in data["result"]
    assert "to_balance" in data["result"]

def test_transfer_insufficient():
    token = get_demo_token()
    # attempt large transfer
    resp = client.post("/accounts/transfer", json={"recipient": "john", "amount": 999999}, headers={"Authorization": token})
    assert resp.status_code == 400
    assert "Insufficient funds" in resp.json()["detail"]
