"""
Test root endpoint redirect functionality.
Verifies GET / redirects to /static/index.html
"""

import pytest


class TestRootRedirect:
    """Tests for the root endpoint (/) redirect."""

    def test_root_redirect_to_static_index(self, client):
        """
        Arrange: Create test client
        Act: Make GET request to /
        Assert: Response is 307 redirect to /static/index.html
        """
        # Arrange
        expected_status = 307
        expected_location = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == expected_status
        assert response.headers["location"] == expected_location

    def test_root_redirect_follow(self, client):
        """
        Arrange: Create test client
        Act: Make GET request to / with follow_redirects=True
        Assert: Final response is 200 OK
        """
        # Arrange & Act
        response = client.get("/", follow_redirects=True)

        # Assert
        assert response.status_code == 200
