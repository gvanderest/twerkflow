"""Tests for DriverFactory."""

from unittest.mock import MagicMock
import pytest
from src.core.driver_factory import DriverFactory, DriverFactoryConfig


def test_driver_factory_full():
    """Verifies full DriverFactory configuration and instantiation."""
    # Mock settings
    mock_settings = MagicMock()

    def get_config(key):
        if key == "task_service":
            return type(
                "Config",
                (),
                {
                    "type": "github_issues",
                    "params": {"repo_name": "test/repo", "token": "fake"},
                },
            )()
        elif key == "doc_service":
            return type(
                "Config",
                (),
                {"type": "notion", "params": {"page_id": "1", "token": "fake"}},
            )()
        elif key == "pr_service":
            return type(
                "Config",
                (),
                {
                    "type": "github_pr",
                    "params": {"repo_name": "test/repo", "token": "fake"},
                },
            )()
        return None

    mock_settings.get_driver_config.side_effect = get_config

    # Mock classes
    mock_task = MagicMock()
    mock_notion = MagicMock()
    mock_pr = MagicMock()
    mock_github_client = MagicMock()

    # Define factory class mocks
    def task_service_factory(repo):
        return mock_task

    def doc_service_factory(token):
        return mock_notion

    def pr_service_factory():
        return mock_pr

    # Use Dependency Injection
    factory_config = DriverFactoryConfig(
        settings=mock_settings,
        task_service_class=task_service_factory,
        doc_service_class=doc_service_factory,
        pr_service_class=pr_service_factory,
        github_client_class=lambda token: mock_github_client,
    )
    factory = DriverFactory(config=factory_config)

    assert factory.get_task_service() == mock_task
    assert factory.get_doc_service() == mock_notion
    assert factory.get_pr_service() == mock_pr


def test_driver_factory_unknown_task_driver():
    """Verifies unknown task driver raises ValueError."""
    mock_settings = MagicMock()
    mock_settings.get_driver_config.return_value = type("Config", (), {"type": "unknown", "params": {}})()

    factory = DriverFactory(config=DriverFactoryConfig(settings=mock_settings))
    with pytest.raises(ValueError, match="Unknown task driver"):
        factory.get_task_service()


def test_driver_factory_unknown_doc_driver():
    """Verifies unknown doc driver raises ValueError."""
    mock_settings = MagicMock()
    mock_settings.get_driver_config.return_value = type("Config", (), {"type": "unknown", "params": {}})()

    factory = DriverFactory(config=DriverFactoryConfig(settings=mock_settings))
    with pytest.raises(ValueError, match="Unknown doc driver"):
        factory.get_doc_service()


def test_driver_factory_unknown_pr_driver():
    """Verifies unknown PR driver raises ValueError."""
    mock_settings = MagicMock()
    mock_settings.get_driver_config.return_value = type("Config", (), {"type": "unknown", "params": {}})()

    factory = DriverFactory(config=DriverFactoryConfig(settings=mock_settings))
    with pytest.raises(ValueError, match="Unknown pr driver"):
        factory.get_pr_service()


def test_driver_factory_missing_token():
    """Verifies missing token raises ValueError."""
    mock_settings = MagicMock()
    mock_settings.get_driver_config.return_value = type(
        "Config",
        (),
        {
            "type": "github_issues",
            "params": {"repo_name": "test/repo", "token": None},
        },
    )()

    # Mock Config class
    mock_config = MagicMock()
    mock_config.token = None
    mock_config.repo_name = "test/repo"

    factory = DriverFactory(
        config=DriverFactoryConfig(settings=mock_settings, config_class=lambda **kwargs: mock_config)
    )
    # The error comes from GitHubIssueConfig validation
    with pytest.raises(ValueError):
        factory.get_task_service()
