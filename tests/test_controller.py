import pytest
from flask import Flask
from unittest.mock import patch
import controller

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


# -------------------------
# login
# -------------------------

def test_login_user_not_found(app):
    with app.app_context():
        with patch("controller.get_users", return_value=[]):
            response, status = controller.login("notfound@example.com", "password")

    assert status == 401
    assert response.get_json() == {"message": "User not found"}


def test_login_success():
    fake_user = {
        "id": "user1",
        "role": "host",
        "email": "test@example.com",
        "password_hash": "hashed-password",
        "name": "Test User",
    }

    with patch("controller.get_users", return_value=[fake_user]), \
         patch("controller.password_helper.verify_password", return_value=True), \
         patch("controller.auth_utils.generate_jwt", return_value="fake-jwt-token"):

        result = controller.login("test@example.com", "password")

    assert result["token"] == "fake-jwt-token"
    assert result["user"]["user_id"] == "user1"
    assert result["user"]["role"] == "host"
    assert result["user"]["email"] == "test@example.com"
    assert result["user"]["name"] == "Test User"


def test_login_invalid_password():
    fake_user = {
        "id": "user1",
        "role": "host",
        "email": "test@example.com",
        "password_hash": "hashed-password",
        "name": "Test User",
    }

    with patch("controller.get_users", return_value=[fake_user]), \
         patch("controller.password_helper.verify_password", return_value=False):

        result = controller.login("test@example.com", "wrong-password")

    assert result is None


# -------------------------
# get_user / get_users
# -------------------------

def test_get_user_calls_dal():
    fake_user = {"id": "user1", "name": "Test User"}

    with patch("controller.users_dal.get_user", return_value=fake_user) as mock_get_user:
        result = controller.get_user("user1")

    mock_get_user.assert_called_once_with("user1")
    assert result == fake_user


def test_get_users_calls_dal():
    fake_users = [{"id": "user1"}, {"id": "user2"}]

    with patch("controller.users_dal.get_users", return_value=fake_users) as mock_get_users:
        result = controller.get_users("Razzo", "test@example.com", "host", True)

    mock_get_users.assert_called_once_with("Razzo", "test@example.com", "host", True)
    assert result == fake_users


# -------------------------
# create_user
# -------------------------

def test_create_user_hashes_password_before_dal_call():
    with patch("controller.password_helper.hash_password", return_value="hashed-password") as mock_hash, \
         patch("controller.users_dal.create_user", return_value={"id": "user1"}) as mock_create:

        result = controller.create_user("Test User", "test@example.com", "plain-password", "host")

    mock_hash.assert_called_once_with("plain-password")
    mock_create.assert_called_once_with("Test User", "test@example.com", "hashed-password", "host")
    assert result == {"id": "user1"}


def test_create_user_without_password_skips_hashing():
    with patch("controller.password_helper.hash_password") as mock_hash, \
         patch("controller.users_dal.create_user", return_value={"id": "user1"}) as mock_create:

        result = controller.create_user("Test User", "test@example.com", None, "host")

    mock_hash.assert_not_called()
    mock_create.assert_called_once_with("Test User", "test@example.com", None, "host")
    assert result == {"id": "user1"}


# -------------------------
# update_user
# -------------------------

def test_update_user_hashes_password_before_dal_call():
    with patch("controller.password_helper.hash_password", return_value="hashed-password") as mock_hash, \
         patch("controller.users_dal.update_user", return_value={"id": "user1"}) as mock_update:

        result = controller.update_user(
            "user1",
            name="Updated Name",
            email="updated@example.com",
            password="plain-password",
            role="performer"
        )

    mock_hash.assert_called_once_with("plain-password")
    mock_update.assert_called_once_with(
        "user1",
        "Updated Name",
        "updated@example.com",
        "hashed-password",
        "performer"
    )
    assert result == {"id": "user1"}


def test_update_user_without_password_skips_hashing():
    with patch("controller.password_helper.hash_password") as mock_hash, \
         patch("controller.users_dal.update_user", return_value={"id": "user1"}) as mock_update:

        result = controller.update_user(
            "user1",
            name="Updated Name",
            email="updated@example.com",
            password=None,
            role="performer"
        )

    mock_hash.assert_not_called()
    mock_update.assert_called_once_with(
        "user1",
        "Updated Name",
        "updated@example.com",
        None,
        "performer"
    )
    assert result == {"id": "user1"}


# -------------------------
# events
# -------------------------

@pytest.mark.parametrize(
    "active_input, expected_active",
    [
        ("true", True),
        ("false", False),
        (None, None),
    ],
)
def test_get_events_converts_active_param(active_input, expected_active):
    fake_events = [{"id": "event1"}]

    with patch("controller.events_dal.get_events", return_value=fake_events) as mock_get_events:
        result = controller.get_events(
            host_id="host1",
            active=active_input,
            location="Atlanta",
            venue_id="venue1",
            date_start="2026-03-01",
            date_end="2026-03-31",
            page_number=1
        )

    mock_get_events.assert_called_once_with(
        "host1",
        expected_active,
        "Atlanta",
        "venue1",
        "2026-03-01",
        "2026-03-31",
        1
    )
    assert result == fake_events


def test_get_event_calls_dal():
    fake_event = {"id": "event1", "title": "My Event"}

    with patch("controller.events_dal.get_event", return_value=fake_event) as mock_get_event:
        result = controller.get_event("event1")

    mock_get_event.assert_called_once_with("event1")
    assert result == fake_event


def test_create_event_calls_dal():
    fake_event = {"id": "event1"}

    with patch("controller.events_dal.create_event", return_value=fake_event) as mock_create:
        result = controller.create_event("host1", "venue1", "Title", "Description", "2026-03-20")

    mock_create.assert_called_once_with("host1", "venue1", "Title", "Description", "2026-03-20")
    assert result == fake_event


def test_update_event_calls_dal():
    fake_event = {"id": "event1", "title": "Updated"}

    with patch("controller.events_dal.update_event", return_value=fake_event) as mock_update:
        result = controller.update_event(
            "event1",
            title="Updated",
            date="2026-03-20",
            venue_id="venue1",
            description="New desc",
            is_active=True
        )

    mock_update.assert_called_once_with(
        "event1",
        "Updated",
        "2026-03-20",
        "venue1",
        "New desc",
        True
    )
    assert result == fake_event


# -------------------------
# applications / performers
# -------------------------

def test_get_event_performers_returns_only_approved_users():
    fake_applications = [
        {"performer_id": "perf1", "status": "approved"},
        {"performer_id": "perf2", "status": "pending"},
        {"performer_id": "perf3", "status": "approved"},
    ]

    with patch("controller.applications_dal.get_applications", return_value=fake_applications) as mock_get_apps, \
         patch("controller.users_dal.get_user", side_effect=[
             {"id": "perf1", "name": "Performer One"},
             {"id": "perf3", "name": "Performer Three"},
         ]) as mock_get_user:

        result = controller.get_event_performers("event1")

    mock_get_apps.assert_called_once_with("event1", None, None)
    assert mock_get_user.call_count == 2
    mock_get_user.assert_any_call("perf1")
    mock_get_user.assert_any_call("perf3")
    assert result == [
        {"id": "perf1", "name": "Performer One"},
        {"id": "perf3", "name": "Performer Three"},
    ]


def test_get_applications_calls_dal():
    fake_applications = [{"id": "app1"}]

    with patch("controller.applications_dal.get_applications", return_value=fake_applications) as mock_get_apps:
        result = controller.get_applications("event1", "perf1", "approved")

    mock_get_apps.assert_called_once_with("event1", "perf1", "approved")
    assert result == fake_applications


def test_get_application_calls_dal():
    fake_application = {"id": "app1"}

    with patch("controller.applications_dal.get_application", return_value=fake_application) as mock_get_app:
        result = controller.get_application("app1")

    mock_get_app.assert_called_once_with("app1")
    assert result == fake_application


def test_create_application_calls_dal():
    fake_application = {"id": "app1"}

    with patch("controller.applications_dal.create_application", return_value=fake_application) as mock_create:
        result = controller.create_application("event1", "perf1")

    mock_create.assert_called_once_with("event1", "perf1")
    assert result == fake_application


def test_update_application_calls_dal():
    fake_application = {"id": "app1", "status": "approved"}

    with patch("controller.applications_dal.update_application", return_value=fake_application) as mock_update:
        result = controller.update_application("app1", "approved")

    mock_update.assert_called_once_with("app1", "approved")
    assert result == fake_application


# -------------------------
# venues
# -------------------------

def test_get_venue_calls_dal():
    fake_venue = {"id": "venue1", "name": "Main Hall"}

    with patch("controller.venues_dal.get_venue", return_value=fake_venue) as mock_get_venue:
        result = controller.get_venue("venue1")

    mock_get_venue.assert_called_once_with("venue1")
    assert result == fake_venue


def test_get_venues_calls_dal():
    fake_venues = [{"id": "venue1"}, {"id": "venue2"}]

    with patch("controller.venues_dal.get_venues", return_value=fake_venues) as mock_get_venues:
        result = controller.get_venues()

    mock_get_venues.assert_called_once_with()
    assert result == fake_venues