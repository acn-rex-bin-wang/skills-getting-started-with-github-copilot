"""
Pytest configuration and shared fixtures for FastAPI tests.
Provides TestClient and sample activity data for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Provides sample activity data for testing.
    Returns a dictionary mimicking the app's activities structure.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
    }


@pytest.fixture
def app_with_test_data(client, sample_activities, monkeypatch):
    """
    Fixture that injects sample activities into the app for testing.
    Uses monkeypatch to temporarily replace the app's activities dict.
    """
    from src import app as app_module
    monkeypatch.setattr(app_module, "activities", sample_activities)
    return client
