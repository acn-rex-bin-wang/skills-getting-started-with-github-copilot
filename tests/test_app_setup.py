"""
Test app initialization and setup.
Verifies FastAPI app is properly configured with static file mounting.
"""

import pytest
from src.app import app


class TestAppSetup:
    """Tests for FastAPI app initialization and configuration."""

    def test_app_exists(self):
        """
        Arrange: Import app module
        Act: Check if app object exists
        Assert: app is a FastAPI instance
        """
        # Arrange & Act
        assert app is not None

        # Assert
        assert hasattr(app, "openapi")
        assert hasattr(app, "routes")

    def test_app_has_correct_title(self):
        """
        Arrange: Access app configuration
        Act: Retrieve app title
        Assert: Title matches expected value
        """
        # Arrange & Act
        title = app.title

        # Assert
        assert title == "Mergington High School API"

    def test_app_static_files_mounted(self):
        """
        Arrange: Access app routes
        Act: Check for StaticFiles mount
        Assert: Static files are mounted at /static
        """
        # Arrange & Act
        routes = app.routes

        # Assert
        static_mounted = any(
            hasattr(route, "path") and route.path == "/static" for route in routes
        )
        assert static_mounted, "Static files not mounted at /static"

    def test_root_endpoint_exists(self):
        """
        Arrange: Access app routes
        Act: Check for root endpoint
        Assert: Root endpoint (/) is defined
        """
        # Arrange & Act
        routes = app.routes

        # Assert
        root_route_exists = any(
            hasattr(route, "path") and route.path == "/" for route in routes
        )
        assert root_route_exists, "Root endpoint (/) not defined"
