# tests/test_auth.py
import pytest
import jwt
from datetime import datetime, timedelta

# Import the Flask app object that you create in main.py
from Main import app          # <-- change if your entry file is named differently

# ---- Config -------------------------------------------------------------

SECRET_KEY = "razzo"   # keep in sync with main code
ROUTE = "/api/venue/events"      # the protected endpoint

# ---- Helpers ------------------------------------------------------------

def make_token(user_id="test-id", role="venue", minutes=5):
    """Create a JWT that expires in <minutes> (negative => already expired)."""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=minutes)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# ---- Fixtures -----------------------------------------------------------

@pytest.fixture
def client():
    """Flask test client (sets app.testing = True)."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

# ---- Tests --------------------------------------------------------------

def test_missing_token(client):
    res = client.get(ROUTE)
    assert res.status_code == 401
    assert b"Token is missing" in res.data

def test_bad_format(client):
    res = client.get(ROUTE, headers={"Authorization": "abc123"})
    assert res.status_code == 401

def test_expired_token(client):
    token = make_token(minutes=-5)                      # already expired
    res = client.get(ROUTE, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401
    assert b"expired" in res.data.lower()

def test_corrupted_token(client):
    token = make_token() + "corrupt"                    # break the signature
    res = client.get(ROUTE, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 401
    assert b"invalid" in res.data.lower()

def test_wrong_role(client):
    token = make_token(role="performer")                # venue-only route
    res = client.get(ROUTE, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code in (401, 403)                # whichever you return
                                                        # adjust expectation

def test_valid_token(client):
    token = make_token()                                # venue role, valid
    res = client.get(ROUTE, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    # Optionally assert structure of returned JSON