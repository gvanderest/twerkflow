"""Tests for settings."""

import os
from src.core.settings import Settings, validate_environment
import pytest


def test_settings_validation():
    """Test driver validation."""
    data = {"context": "test", "drivers": {"task_service": "github", "doc_service": "wiki", "pr_service": "pr"}}
    settings = Settings(**data)
    assert settings.get_driver_config("task_service").type == "github"

    with pytest.raises(ValueError, match="Missing required driver"):
        Settings(context="test", drivers={})


def test_validate_environment():
    """Test environment validation."""
    os.environ["GITHUB_TOKEN"] = "token"
    validate_environment()

    del os.environ["GITHUB_TOKEN"]
    with pytest.raises(EnvironmentError):
        validate_environment()
