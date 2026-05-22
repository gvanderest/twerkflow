import pytest
import os
from src.drivers.config import (
    GitHubIssueConfig,
    AsanaConfig,
    NotionConfig,
    GitHubPRConfig,
    GitHubWikiConfig,
)


def test_github_issue_config_success():
    os.environ["GITHUB_TOKEN"] = "test_token"
    config = GitHubIssueConfig(repo_name="test/repo")
    assert config.repo_name == "test/repo"
    assert config.token.get_secret_value() == "test_token"


def test_github_issue_config_missing_env():
    if "GITHUB_TOKEN" in os.environ:
        del os.environ["GITHUB_TOKEN"]
    with pytest.raises(ValueError, match="GITHUB_TOKEN environment variable not set"):
        GitHubIssueConfig(repo_name="test/repo")


def test_asana_config_success():
    os.environ["ASANA_PAT"] = "test_pat"
    config = AsanaConfig(project_gid="123")
    assert config.project_gid == "123"
    assert config.token.get_secret_value() == "test_pat"


def test_asana_config_missing_env():
    if "ASANA_PAT" in os.environ:
        del os.environ["ASANA_PAT"]
    with pytest.raises(ValueError, match="ASANA_PAT environment variable not set"):
        AsanaConfig(project_gid="123")


def test_notion_config_success():
    os.environ["NOTION_API_KEY"] = "test_key"
    config = NotionConfig(page_id="123")
    assert config.page_id == "123"
    assert config.token.get_secret_value() == "test_key"


def test_notion_config_missing_env():
    if "NOTION_API_KEY" in os.environ:
        del os.environ["NOTION_API_KEY"]
    with pytest.raises(ValueError, match="NOTION_API_KEY environment variable not set"):
        NotionConfig(page_id="123")


def test_github_pr_config_success():
    os.environ["GITHUB_TOKEN"] = "test_token"
    config = GitHubPRConfig(repo_name="test/repo")
    assert config.repo_name == "test/repo"
    assert config.token.get_secret_value() == "test_token"


def test_github_wiki_config():
    config = GitHubWikiConfig(wiki_url="https://test.wiki")
    assert config.wiki_url == "https://test.wiki"
