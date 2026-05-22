import pytest
import os
from unittest.mock import patch, MagicMock
from src.core.driver_factory import DriverFactory

@patch("src.core.config_loader.load_settings")
def test_driver_factory_full(mock_load):
    with patch.dict(os.environ, {"GITHUB_TOKEN": "fake", "NOTION_API_KEY": "fake", "ASANA_PAT": "fake"}):
        
        # Mock settings
        def get_config(key):
            if key == 'task_service':
                return type('Config', (), {'type': 'github_issues', 'params': {'repo_name': 'test/repo'}})()
            elif key == 'doc_service':
                return type('Config', (), {'type': 'notion', 'params': {'page_id': '1'}})()
            elif key == 'pr_service':
                return type('Config', (), {'type': 'github_pr', 'params': {'repo_name': 'test/repo'}})()
            return None
        
        mock_load.return_value.get_driver_config.side_effect = get_config
        
        with patch("src.core.driver_factory.GitHubIssueTaskService") as mock_task,              patch("src.core.driver_factory.NotionDocService") as mock_notion,              patch("src.core.driver_factory.GitHubPRService") as mock_pr:
             
            factory = DriverFactory()
            
            assert factory.get_task_service() == mock_task.return_value
            assert factory.get_doc_service() == mock_notion.return_value
            assert factory.get_pr_service() == mock_pr.return_value
            
            mock_task.assert_called_once()
            mock_notion.assert_called_once()
            mock_pr.assert_called_once()
