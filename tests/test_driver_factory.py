import pytest
import os
from unittest.mock import MagicMock
from src.core.driver_factory import DriverFactory
from src.core.config_loader import load_settings

def test_driver_factory_full(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "fake")
    monkeypatch.setenv("NOTION_API_KEY", "fake")
    monkeypatch.setenv("ASANA_PAT", "fake")
    
    # Mock settings
    mock_settings = MagicMock()
    def get_config(key):
        if key == 'task_service':
            return type('Config', (), {'type': 'github_issues', 'params': {'repo_name': 'test/repo', 'token': 'fake'}})()
        elif key == 'doc_service':
            return type('Config', (), {'type': 'notion', 'params': {'page_id': '1', 'token': 'fake'}})()
        elif key == 'pr_service':
            return type('Config', (), {'type': 'github_pr', 'params': {'repo_name': 'test/repo', 'token': 'fake'}})()
        return None
    
    mock_settings.get_driver_config.side_effect = get_config
    monkeypatch.setattr("src.core.driver_factory.load_settings", lambda: mock_settings)
    
    # Mock classes
    mock_task = MagicMock()
    mock_notion = MagicMock()
    mock_pr = MagicMock()
    
    monkeypatch.setattr("src.core.driver_factory.GitHubIssueTaskService", lambda repo: mock_task)
    monkeypatch.setattr("src.core.driver_factory.NotionDocService", lambda token: mock_notion)
    monkeypatch.setattr("src.core.driver_factory.GitHubPRService", lambda: mock_pr)
    monkeypatch.setattr("src.core.driver_factory.GitHubWikiDocService", lambda: MagicMock())
    monkeypatch.setattr("src.core.driver_factory.Github", MagicMock())
             
    factory = DriverFactory()
    
    assert factory.get_task_service() == mock_task
    assert factory.get_doc_service() == mock_notion
    assert factory.get_pr_service() == mock_pr
