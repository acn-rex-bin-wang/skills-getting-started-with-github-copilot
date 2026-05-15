"""
Test GET /activities endpoint.
Verifies activities list is returned correctly with proper structure.
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_200(self, app_with_test_data):
        """
        Arrange: Create test client with sample activities
        Act: Make GET request to /activities
        Assert: Response status is 200 OK
        """
        # Arrange
        client = app_with_test_data

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, app_with_test_data):
        """
        Arrange: Create test client with sample activities
        Act: Make GET request to /activities
        Assert: Response is a JSON dictionary
        """
        # Arrange
        client = app_with_test_data

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_all_activities(self, app_with_test_data):
        """
        Arrange: Create test client with sample activities
        Act: Make GET request to /activities
        Assert: Response contains all expected activities
        """
        # Arrange
        client = app_with_test_data
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity in expected_activities:
            assert activity in data

    def test_get_activities_has_correct_structure(self, app_with_test_data):
        """
        Arrange: Create test client with sample activities
        Act: Make GET request to /activities
        Assert: Each activity has required fields (description, schedule, max_participants, participants)
        """
        # Arrange
        client = app_with_test_data
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Missing field '{field}' in activity '{activity_name}'"

    def test_get_activities_participants_is_list(self, app_with_test_data):
        """
        Arrange: Create test client with sample activities
        Act: Make GET request to /activities
        Assert: participants field is a list for each activity
        """
        # Arrange
        client = app_with_test_data

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"participants not a list in '{activity_name}'"

    def test_get_activities_correct_participant_count(self, app_with_test_data):
        """
        Arrange: Create test client with sample activities
        Act: Make GET request to /activities
        Assert: Specific activities have correct participant counts
        """
        # Arrange
        client = app_with_test_data

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert len(data["Chess Club"]["participants"]) == 2
        assert len(data["Programming Class"]["participants"]) == 1
        assert len(data["Gym Class"]["participants"]) == 0
