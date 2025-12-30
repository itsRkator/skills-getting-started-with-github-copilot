from fastapi.testclient import TestClient
import pytest

from src import app as app_module

client = TestClient(app_module.app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    # Basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    email = "testuser@example.com"

    # Ensure email not present initially
    r = client.get("/activities")
    assert r.status_code == 200
    assert email not in r.json()[activity]["participants"]

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json()["message"]

    # Now participant should be present
    r = client.get("/activities")
    assert email in r.json()[activity]["participants"]

    # Unregister
    r = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r.status_code == 200
    assert "Unregistered" in r.json()["message"]

    # Ensure removed
    r = client.get("/activities")
    assert email not in r.json()[activity]["participants"]


def test_double_signup_returns_400():
    activity = "Chess Club"
    email = "daniel@mergington.edu"  # already in initial data

    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 400


def test_unregister_nonexistent_returns_404():
    activity = "Chess Club"
    email = "noone@example.com"

    r = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r.status_code == 404
