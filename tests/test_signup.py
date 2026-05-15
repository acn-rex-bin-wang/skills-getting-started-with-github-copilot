"""
Test POST /activities/{activity_name}/signup endpoint.
Verifies signup functionality with success cases and error handling.
"""

import pytest


class TestSignupActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, app_with_test_data):
        """
        Arrange: Create test client, identify activity and email
        Act: POST to signup endpoint with valid email and activity
        Assert: Response is 200 OK and success message returned
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Gym Class"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant(self, app_with_test_data):
        """
        Arrange: Create test client, get initial participant count
        Act: POST to signup endpoint
        Assert: Participant count increases by 1
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Gym Class"
        email = "newstudent@mergington.edu"

        # Get initial state
        response = client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Verify participant was added
        response = client.get("/activities")
        new_count = len(response.json()[activity_name]["participants"])
        assert new_count == initial_count + 1
        assert email in response.json()[activity_name]["participants"]

    def test_signup_activity_not_found(self, app_with_test_data):
        """
        Arrange: Create test client with nonexistent activity name
        Act: POST to signup endpoint with invalid activity
        Assert: Response is 404 Not Found
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_signup_already_registered(self, app_with_test_data):
        """
        Arrange: Create test client, use existing participant
        Act: POST to signup endpoint with already-registered email
        Assert: Response is 400 Bad Request
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already" in data["detail"].lower()

    def test_signup_multiple_times_fails(self, app_with_test_data):
        """
        Arrange: Create test client and new email
        Act: POST to signup twice with same email/activity
        Assert: First succeeds (200), second fails (400)
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Gym Class"
        email = "future_student@mergington.edu"

        # Act: First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act: Second signup (same email)
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400

    def test_signup_special_characters_in_email(self, app_with_test_data):
        """
        Arrange: Create test client with email containing special characters
        Act: POST to signup endpoint
        Assert: Signup succeeds and email preserved correctly
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Gym Class"
        email = "student+tag@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        assert email in verify_response.json()[activity_name]["participants"]

    def test_signup_with_url_encoded_activity_name(self, app_with_test_data):
        """
        Arrange: Create test client with activity name containing spaces
        Act: POST to signup endpoint with URL-encoded activity name
        Assert: Signup succeeds
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Programming Class"  # Name with space
        email = "coder@mergington.edu"

        # Act: FastAPI/TestClient handles encoding automatically
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
