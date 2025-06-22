import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json
import Controller

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def mock_dals():
    with patch('Controller.users_data') as users_data_mock, \
         patch('Controller.events_data') as events_data_mock, \
         patch('Controller.venues_data') as venues_data_mock:
        yield users_data_mock, events_data_mock, venues_data_mock

def test_login_user_success(app, mock_dals):
    users_data_mock, _, _ = mock_dals
    fake_user = {
        'id': 'user1',
        'role': 'host',
        'email': 'test@example.com',
        'password': 'hashed-password',
        'name': 'Test User'
    }
    users_data_mock.getUserByEmail.return_value = fake_user

    with patch('Controller.Authentication.authenticate', return_value=True), \
         patch('Controller.Authentication.generateJWT', return_value='fake-jwt-token'), \
         app.app_context():
        response, status = Controller.login_user({
            'email': 'test@example.com',
            'password': 'password'
        })

    assert status == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert data['user']['user_id'] == 'user1'

# Similarly wrap other tests:

def test_login_user_user_not_found(app, mock_dals):
    users_data_mock, _, _ = mock_dals
    users_data_mock.getUserByEmail.return_value = None

    with app.app_context():
        response, status = Controller.login_user({
            'email': 'notfound@example.com',
            'password': 'password'
        })

    assert status == 401
    data = json.loads(response.data)
    assert data['message'] == 'User not found'

def test_get_user_success(app, mock_dals):
    users_data_mock, _, _ = mock_dals
    fake_user_data = {'id': 'user1', 'name': 'Test User'}
    users_data_mock.get_user.return_value = fake_user_data

    with app.app_context():
        response, status = Controller.get_user('user1')

    assert status == 200
    data = json.loads(response.data)
    assert data['id'] == 'user1'

# def test_create_user_success(app, mock_dals):
#     with patch('Controller.Models.User.User') as MockUser, app.app_context():
#         mock_user_instance = MagicMock()
#         mock_user_instance.userName = "johndoe"
#         mock_user_instance.password = "hashedpass"
#         MockUser.return_value = mock_user_instance

#         request_body = {
#             "firstName": "John",
#             "lastName": "Doe",
#             "email": "john@example.com",
#             "userName": "johndoe",
#             "password": "password123",
#             "age": 30
#         }

#         response, status = Controller.create_user(request_body)

#     assert status == 200
#     data = json.loads(response.data)
#     assert data["userName"] == "johndoe"
#     assert data["password"] == "hashedpass"
#     mock_users_dal.addUser.assert_called_once_with(mock_user_instance)

@pytest.mark.parametrize("missing_field", ["firstName", "email", "userName", "password", "age"])
def test_create_user_missing_fields(app, missing_field):
    with app.app_context():
        body = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "userName": "johndoe",
            "password": "password123",
            "age": 30
        }
        del body[missing_field]

        response, status = Controller.create_user(body)

    assert status == 400
    data = json.loads(response.data)
    assert f"Missing or empty required field: {missing_field}" in data["error"]

def test_create_user_invalid_age_string(app):
    body = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "userName": "johndoe",
        "password": "password123",
        "age": "not-a-number"
    }
    with app.app_context():
        response, status = Controller.create_user(body)

    assert status == 400
    assert b'Age must be a valid integer' in response.data

def test_create_user_negative_age(app):
    body = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "userName": "johndoe",
        "password": "password123",
        "age": -5
    }
    with app.app_context():
        response, status = Controller.create_user(body)

    assert status == 400
    assert b'Age must be a positive number' in response.data


# Continue for other tests...
