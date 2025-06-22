# tests/test_auth.py

import pytest
import jwt
from datetime import datetime, timedelta
from Main import app  # ensure this points to your Flask app

# ---------- Constants ----------
SECRET_KEY = "Secret_key"  # Sync with your real secret key
ROUTE = "/events"     # Protected route to test token logic

# ---------- Helper: Token Generator ----------
def make_token(user_id="test-id", role="host", minutes=5):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=minutes)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# ---------- Pytest Fixture ----------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

# ---------- Tests ----------

def test_missing_token(client):
    res = client.get(ROUTE)
    assert res.status_code == 401
    assert b"Token is missing" in res.data

def test_bad_format(client):
    res = client.get(ROUTE, headers={"Authorization": "JustSomeString"})
    assert res.status_code == 401

def test_expired_token(client):
    token = make_token(minutes=-10)  # Already expired
    res = client.get(ROUTE, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401
    assert b"expired" in res.data.lower()

def test_invalid_token(client):
    token = make_token() + "garbage"
    res = client.get(ROUTE, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401
    assert b"invalid" in res.data.lower()

def test_valid_token(client):
    token = make_token()
    res = client.get(ROUTE, headers={"Authorization": f"Bearer {token}"})
    
    # If your data source is empty, this might return 200 with []
    assert res.status_code == 200 or res.status_code == 204
