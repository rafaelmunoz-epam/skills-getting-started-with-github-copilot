import os
import sys
from fastapi.testclient import TestClient

# Ensure src is on the path so we can import the app module
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import app as app_module

client = TestClient(app_module.app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Spot-check a known activity from the seed data
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_student@example.com"

    # Make sure test email isn't already present
    participants = app_module.activities[activity]["participants"]
    if email in participants:
        participants.remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Signing up again should return a 400
    resp_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp_unreg.status_code == 200
    assert email not in app_module.activities[activity]["participants"]

    # Unregistering again should 400
    resp_unreg2 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp_unreg2.status_code == 400
