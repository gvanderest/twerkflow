import pytest
import os
from unittest.mock import patch, MagicMock
from src.core.driver_factory import DriverFactory

@patch("src.core.driver_factory.Github")
@patch("src.core.config_loader.load_settings")
def test_driver_factory_full(mock_load, mock_github):
    os.environ["GITHUB_TOKEN"] = "fake"
    # Mock settings to return different drivers
    mock_load.return_value.get_driver_config.side_effect = lambda key: type(
        'Config', (), {
            'type': 'github_issues' if key == 'task_service' else 'notion',
            'params': {'repo_name': 'test/repo'}
        }
    )()
    
    factory = DriverFactory()
    
    # Test all methods
    assert factory.get_task_service().__class__.__name__ == "GitHubIssueTaskService"
    assert factory.get_doc_service().__class__.__name__ == "NotionDocService"
    # mock_github should be called for GitHubIssueTaskService
    mock_github.assert_called()

@patch("src.core.driver_factory.Github")
@patch("src.core.config_loader.load_settings")
def test_driver_factory_asana(mock_load, mock_github):
    os.environ["GITHUB_TOKEN"] = "fake"
    mock_load.return_value.get_driver_config.side_effect = lambda key: type(
        'Config', (), {
            'type': 'asana',
            'params': {'project_gid': '123'}
        }
    )()
    factory = DriverFactory()
    assert factory.get_task_service().__class__.__name__ == "AsanaTaskService"
    # Github should NOT be called
    mock_github.assert_not_called()
