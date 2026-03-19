import pytest
from unittest.mock import patch
import Main


@pytest.fixture
def flask_app():
    Main.app.config["TESTING"] = True
    return Main.app


@pytest.fixture
def app_context(flask_app):
    with flask_app.app_context():
        yield


@pytest.fixture
def client(flask_app):
    with flask_app.test_client() as client:
        yield client


def test_ping(client):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.get_json() == {"status": "Ok"}


def test_login_success(client):
    fake_result = {
        "token": "fake-jwt-token",
        "user": {
            "user_id": "user1",
            "role": "host",
            "email": "test@example.com",
            "name": "Test User"
        }
    }

    with patch("Main.controller.login", return_value=fake_result) as mock_login:
        response = client.post("/login", json={
            "email": "test@example.com",
            "password": "password123"
        })

    assert response.status_code == 200
    assert response.get_json() == fake_result
    mock_login.assert_called_once_with("test@example.com", "password123")


def test_login_invalid(client):
    with patch("Main.controller.login", return_value=None) as mock_login:
        response = client.post("/login", json={
            "email": "bad@example.com",
            "password": "wrong-password"
        })

    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid Login."}
    mock_login.assert_called_once_with("bad@example.com", "wrong-password")


def test_login_with_empty_json(client):
    with patch("Main.controller.login", return_value=None) as mock_login:
        response = client.post("/login", json={})

    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid Login."}
    mock_login.assert_called_once_with(None, None)


def test_login_with_no_json_body(client):
    with patch("Main.controller.login", return_value=None) as mock_login:
        response = client.post("/login")

    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid Login."}
    mock_login.assert_called_once_with(None, None)


def test_create_user_success(client):
    fake_user = {
        "id": "user1",
        "name": "Test User",
        "email": "test@example.com",
        "role": "host"
    }

    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": "host"
    }

    with patch("Main.controller.create_user", return_value=fake_user) as mock_create_user:
        response = client.post("/users", json=payload)

    assert response.status_code == 201
    assert response.get_json() == fake_user
    mock_create_user.assert_called_once_with(
        name="Test User",
        email="test@example.com",
        password="password123",
        role="host"
    )

def test_get_user_protected_success(app_context):
    fake_user = {"id": "user1", "name": "Test User"}

    with patch("Main.controller.get_user", return_value=fake_user) as mock_get_user:
        response = Main.get_user.__wrapped__("user1")

    mock_get_user.assert_called_once_with("user1")
    assert response.status_code == 200
    assert response.get_json() == fake_user


def test_get_user_protected_not_found(app_context):
    with patch("Main.controller.get_user", return_value=None) as mock_get_user:
        response, status = Main.get_user.__wrapped__("user1")

    mock_get_user.assert_called_once_with("user1")
    assert status == 404
    assert response.get_json() == {"error": "User not found"}


def test_get_users_protected_success(flask_app):
    fake_users = [{"id": "user1"}, {"id": "user2"}]

    # Note: Main.py currently maps query param 'host_id' into the variable named 'name'
    with flask_app.test_request_context("/users?host_id=Razzo&email=test@example.com&role=host&active=true"):
        with patch("Main.controller.get_users", return_value=fake_users) as mock_get_users:
            response, status = Main.get_users.__wrapped__()

    mock_get_users.assert_called_once_with("Razzo", "test@example.com", "host", "true")
    assert status == 200
    assert response.get_json() == fake_users


def test_update_user_protected_success(flask_app):
    payload = {
        "id": "user1",
        "name": "Updated User",
        "email": "updated@example.com",
        "password": "newpass123",
        "role": "host"
    }

    updated_user = {
        "id": "user1",
        "name": "Updated User",
        "email": "updated@example.com",
        "role": "host"
    }

    with flask_app.test_request_context("/users", method="PUT", json=payload):
        with patch("Main.controller.update_user", return_value=updated_user) as mock_update_user:
            response, status = Main.update_user.__wrapped__()

    mock_update_user.assert_called_once_with(
        "user1",
        "Updated User",
        "updated@example.com",
        "newpass123",
        "host"
    )
    assert status == 200
    assert response.get_json() == updated_user


def test_update_user_protected_not_found(flask_app):
    payload = {
        "id": "user1",
        "name": "Updated User",
        "email": "updated@example.com",
        "password": "newpass123",
        "role": "host"
    }

    with flask_app.test_request_context("/users", method="PUT", json=payload):
        with patch("Main.controller.update_user", return_value=None) as mock_update_user:
            response, status = Main.update_user.__wrapped__()

    mock_update_user.assert_called_once_with(
        "user1",
        "Updated User",
        "updated@example.com",
        "newpass123",
        "host"
    )
    assert status == 404
    assert response.get_json() == {"error": "User not found or update failed"}


def test_get_events_protected_success(flask_app):
    fake_events = [{"id": "event1", "title": "Show Night"}]

    url = "/events?host_id=1&active=true&location=Atlanta&venue_id=2&date_start=2026-03-01&date_end=2026-03-31&page_number=3"

    with flask_app.test_request_context(url, method="GET"):
        with patch("Main.controller.get_events", return_value=fake_events) as mock_get_events:
            response, status = Main.get_events.__wrapped__()

    mock_get_events.assert_called_once_with(
        1,
        "true",
        "Atlanta",
        2,
        "2026-03-01",
        "2026-03-31",
        3
    )
    assert status == 200
    assert response.get_json() == fake_events


def test_get_event_protected_success(app_context):
    fake_event = {"id": "event1", "title": "Main Event"}

    with patch("Main.controller.get_event", return_value=fake_event) as mock_get_event:
        response = Main.get_event.__wrapped__("event1")

    mock_get_event.assert_called_once_with("event1")
    assert response.status_code == 200
    assert response.get_json() == fake_event


def test_get_event_protected_not_found(app_context):
    with patch("Main.controller.get_event", return_value=None) as mock_get_event:
        response, status = Main.get_event.__wrapped__("event1")

    mock_get_event.assert_called_once_with("event1")
    assert status == 404
    assert response.get_json() == {"error": "Event not found"}


def test_get_applications_protected_success(flask_app):
    fake_applications = [{"id": "app1"}, {"id": "app2"}]

    url = "/applications?event_id=10&performer_id=perf1&status=approved"

    with flask_app.test_request_context(url, method="GET"):
        with patch("Main.controller.get_applications", return_value=fake_applications) as mock_get_apps:
            response, status = Main.get_applications.__wrapped__()

    mock_get_apps.assert_called_once_with(10, "perf1", "approved")
    assert status == 200
    assert response.get_json() == fake_applications


def test_get_applications_protected_not_found(flask_app):
    url = "/applications?event_id=10&performer_id=perf1&status=approved"

    with flask_app.test_request_context(url, method="GET"):
        with patch("Main.controller.get_applications", return_value=None) as mock_get_apps:
            response, status = Main.get_applications.__wrapped__()

    mock_get_apps.assert_called_once_with(10, "perf1", "approved")
    assert status == 404
    assert response.get_json() == {"message": "No events found"}


def test_get_application_protected_success(app_context):
    fake_application = {"id": "app1", "status": "approved"}

    with patch("Main.controller.get_application", return_value=fake_application) as mock_get_application:
        response = Main.get_application.__wrapped__("app1")

    mock_get_application.assert_called_once_with("app1")
    assert response.status_code == 200
    assert response.get_json() == fake_application


def test_get_application_protected_not_found(app_context):
    with patch("Main.controller.get_application", return_value=None) as mock_get_application:
        response, status = Main.get_application.__wrapped__("app1")

    mock_get_application.assert_called_once_with("app1")
    assert status == 404
    assert response.get_json() == {"error": "Application not found"}


def test_get_venues_protected_success(app_context):
    fake_venues = [{"id": "venue1"}, {"id": "venue2"}]

    with patch("Main.controller.get_venues", return_value=fake_venues) as mock_get_venues:
        result = Main.get_venues.__wrapped__()

    mock_get_venues.assert_called_once_with()
    assert result == fake_venues