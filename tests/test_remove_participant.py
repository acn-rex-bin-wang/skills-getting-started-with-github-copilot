"""
Test DELETE /activities/{activity_name}/participants endpoint.
Verifies participant removal functionality with success and error cases.
"""

import pytest


class TestRemoveParticipant:
    """Tests for the DELETE /activities/{activity_name}/participants endpoint."""

    def test_remove_participant_success(self, app_with_test_data):
        """
        Arrange: Create test client with existing participant
        Act: DELETE request to remove participant
        Assert: Response is 200 OK and success message returned
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Known participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_participant_is_deleted(self, app_with_test_data):
        """
        Arrange: Create test client, verify initial state
        Act: DELETE request to remove participant
        Assert: Participant count decreases by 1 and email not in list
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Get initial state
        response = client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])
        assert email in response.json()[activity_name]["participants"]

        # Act
        client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        response = client.get("/activities")
        new_count = len(response.json()[activity_name]["participants"])
        assert new_count == initial_count - 1
        assert email not in response.json()[activity_name]["participants"]

    def test_remove_participant_activity_not_found(self, app_with_test_data):
        """
        Arrange: Create test client with nonexistent activity
        Act: DELETE request with invalid activity name
        Assert: Response is 404 Not Found
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_remove_participant_not_found(self, app_with_test_data):
        """
        Arrange: Create test client with nonexistent participant email
        Act: DELETE request with email not in activity
        Assert: Response is 404 Not Found
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]

    def test_remove_last_participant(self, app_with_test_data):
        """
        Arrange: Create test client, remove all but one participant from an activity
        Act: DELETE request to remove the last participant
        Assert: Response is 200, activity has 0 participants
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Only participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        assert len(verify_response.json()[activity_name]["participants"]) == 0

    def test_remove_participant_from_empty_activity(self, app_with_test_data):
        """
        Arrange: Create test client, activity with no participants
        Act: DELETE request to remove participant from empty activity
        Assert: Response is 404 Not Found
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Gym Class"  # Has no participants
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_remove_different_participants_independently(self, app_with_test_data):
        """
        Arrange: Create test client with activity having multiple participants
        Act: DELETE one participant, verify other remains
        Assert: Correct participant removed, others unchanged
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email_to_remove}
        )

        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        participants = verify_response.json()[activity_name]["participants"]
        assert email_to_remove not in participants
        assert email_to_keep in participants

    def test_remove_participant_special_characters_in_email(self, app_with_test_data):
        """
        Arrange: Create test client, add participant with special chars, then remove
        Act: POST signup with special email, then DELETE same email
        Assert: Both operations succeed
        """
        # Arrange
        client = app_with_test_data
        activity_name = "Gym Class"
        email = "student+special@mergington.edu"

        # First add the participant
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Act: Remove the participant
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        verify_response = client.get("/activities")
        assert email not in verify_response.json()[activity_name]["participants"]
