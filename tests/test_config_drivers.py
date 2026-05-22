"""Tests for driver configuration models."""

import os
import pytest
from src.drivers.config import (
    AsanaConfig,
    GitHubIssueConfig,
    GitHubPRConfig,
    GitHubWikiConfig,
    NotionConfig,
)


def test_github_issue_config_success():
    """Verifies GitHubIssueConfig with token."""
    os.environ["GITHUB_TOKEN"] = "test_token"
    config = GitHubIssueConfig(repo_name="test/repo", label_to_search="test_label")
    assert config.repo_name == "test/repo"
    assert config.label_to_search == "test_label"
    assert config.token.get_secret_value() == "test_token"


def test_github_issue_config_missing_env():
    """Verifies GitHubIssueConfig without token raises ValueError."""
    if "GITHUB_TOKEN" in os.environ:
        del os.environ["GITHUB_TOKEN"]
    with pytest.raises(ValueError, match="GITHUB_TOKEN environment variable not set"):
        GitHubIssueConfig(repo_name="test/repo")


def test_asana_config_success():
    """Verifies AsanaConfig with token."""
    os.environ["ASANA_PAT"] = "test_pat"
    config = AsanaConfig(project_gid="123")
    assert config.project_gid == "123"
    assert config.token.get_secret_value() == "test_pat"


def test_asana_config_missing_env():
    """Verifies AsanaConfig without token raises ValueError."""
    if "ASANA_PAT" in os.environ:
        del os.environ["ASANA_PAT"]
    with pytest.raises(ValueError, match="ASANA_PAT environment variable not set"):
        AsanaConfig(project_gid="123")


def test_notion_config_success():
    """Verifies NotionConfig with token."""
    os.environ["NOTION_API_KEY"] = "test_key"
    config = NotionConfig(page_id="123")
    assert config.page_id == "123"
    assert config.token.get_secret_value() == "test_key"


def test_notion_config_missing_env():
    """Verifies NotionConfig without token raises ValueError."""
    if "NOTION_API_KEY" in os.environ:
        del os.environ["NOTION_API_KEY"]
    with pytest.raises(ValueError, match="NOTION_API_KEY environment variable not set"):
        NotionConfig(page_id="123")


def test_github_pr_config_success():
    """Verifies GitHubPRConfig with token."""
    os.environ["GITHUB_TOKEN"] = "test_token"
    config = GitHubPRConfig(repo_name="test/repo")
    assert config.repo_name == "test/repo"
    assert config.token.get_secret_value() == "test_token"


def test_github_wiki_config():
    """Verifies GitHubWikiConfig."""
    config = GitHubWikiConfig(wiki_url="https://test.wiki")
    assert config.wiki_url == "https://test.wiki"
