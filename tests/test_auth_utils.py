import pytest
import jwt
from flask import Flask, jsonify, request
from unittest.mock import patch

import auth_utils


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True

    @app.route("/protected")
    @auth_utils.token_required
    def protected():
        return jsonify({
            "message": "success",
            "user_id": getattr(request, "user_id", None),
            "user_role": getattr(request, "user_role", None)
        }), 200

    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_token_required_missing_token(client):
    response = client.get("/protected")

    assert response.status_code == 401
    assert response.get_json() == {"message": "Token is missing!"}


def test_token_required_header_without_bearer_prefix(client):
    response = client.get("/protected", headers={
        "Authorization": "Token abc123"
    })

    assert response.status_code == 401
    assert response.get_json() == {"message": "Token is missing!"}


def test_token_required_valid_token(client):
    decoded_payload = {
        "user_id": "user1",
        "role": "host"
    }

    with patch("auth_utils.jwt.decode", return_value=decoded_payload) as mock_decode:
        response = client.get("/protected", headers={
            "Authorization": "Bearer good-token"
        })

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "success",
        "user_id": "user1",
        "user_role": "host"
    }
    mock_decode.assert_called_once_with(
        "good-token",
        auth_utils.SECRET_KEY,
        algorithms=["HS256"]
    )


def test_token_required_expired_token(client):
    with patch("auth_utils.jwt.decode", side_effect=jwt.ExpiredSignatureError):
        response = client.get("/protected", headers={
            "Authorization": "Bearer expired-token"
        })

    assert response.status_code == 401
    assert response.get_json() == {"message": "Token has expired!"}


def test_token_required_invalid_token(client):
    with patch("auth_utils.jwt.decode", side_effect=jwt.InvalidTokenError):
        response = client.get("/protected", headers={
            "Authorization": "Bearer bad-token"
        })

    assert response.status_code == 401
    assert response.get_json() == {"message": "Token is invalid!"}


def test_generate_jwt_calls_encode_with_expected_payload():
    with patch("auth_utils.date_helper.get_token_expiration", return_value=1234567890) as mock_exp, \
         patch("auth_utils.jwt.encode", return_value="fake-jwt-token") as mock_encode:

        token = auth_utils.generate_jwt("user1", "host")

    assert token == "fake-jwt-token"
    mock_exp.assert_called_once_with()
    mock_encode.assert_called_once_with(
        {
            "user_id": "user1",
            "role": "host",
            "exp": 1234567890
        },
        "Secret_key",
        algorithm="HS256"
    )