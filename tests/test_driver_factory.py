import pytest
import os
from unittest.mock import patch, MagicMock
from src.core.driver_factory import DriverFactory
from src.drivers.github_issues import GitHubIssueTaskService

@patch("src.core.driver_factory.Github")
@patch("src.core.config_loader.load_settings")
def test_driver_factory_full(mock_load, mock_github):
    os.environ["GITHUB_TOKEN"] = "fake"
    # Mock settings to return different drivers
    mock_load.return_value.get_driver_config.side_effect = lambda key: type(
        'Config', (), {
            'type': 'asana' if key == 'task_service' else 'notion'
            if key == 'doc_service' else 'github_pr',
            'params': {'repo_name': 'test/repo'}
        }
    )()
    
    factory = DriverFactory()
    
    # Test all methods
    assert factory.get_task_service().__class__.__name__ == "GitHubIssueTaskService"
    assert factory.get_doc_service().__class__.__name__ == "NotionDocService"
    assert factory.get_pr_service().__class__.__name__ == "GitHubPRService"

@patch("src.core.config_loader.load_settings")
def test_driver_factory_asana(mock_load):
    os.environ["GITHUB_TOKEN"] = "fake"
    mock_load.return_value.get_driver_config.side_effect = lambda key: type(
        'Config', (), {
            'type': 'asana',
            'params': {}
        }
    )()
    factory = DriverFactory()
    assert factory.get_task_service().__class__.__name__ == "AsanaTaskService"
