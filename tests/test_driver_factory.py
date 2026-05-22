import pytest
import os
from unittest.mock import patch
from src.core.driver_factory import DriverFactory

@patch("src.core.config_loader.load_settings")
def test_driver_factory(mock_load):
    os.environ["GITHUB_TOKEN"] = "fake"
    # Mock settings
    mock_load.return_value.get_driver_config.side_effect = lambda key: type('Config', (), {'type': 'asana' if key == 'task_service' else 'notion' if key == 'doc_service' else 'github_pr'})()
    
    factory = DriverFactory()
    assert factory.get_task_service().__class__.__name__ == "AsanaTaskService"
    assert factory.get_doc_service().__class__.__name__ == "NotionDocService"
    assert factory.get_pr_service().__class__.__name__ == "GitHubPRService"
