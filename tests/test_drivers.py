import pytest
from unittest.mock import MagicMock, patch
from src.drivers.github_issues import GitHubIssueTaskService

@patch("src.drivers.github_issues.Github")
def test_github_issue_driver_scope(mock_github_class):
    # Setup mock
    mock_github_instance = MagicMock()
    mock_repo = MagicMock()
    mock_github_class.return_value = mock_github_instance
    mock_github_instance.get_repo.return_value = mock_repo
    
    # Target repository for test
    test_repo = "gvanderest/twerkflow"
    
    # Initialize driver
    driver = GitHubIssueTaskService(repo_name=test_repo)
    
    # Verify it scoped to the correct repo immediately upon initialization
    mock_github_instance.get_repo.assert_called_once_with(test_repo)
    
    # Test task retrieval
    mock_repo.get_issue.return_value = MagicMock(
        number=123, 
        title="Test Issue", 
        body="Body", 
        state="open", 
        labels=[]
    )
    
    driver.get_task("123")
    mock_repo.get_issue.assert_called_with(123)

@patch("src.drivers.github_issues.Github")
def test_github_issue_driver_wrong_scope(mock_github_class):
    # Setup mock
    mock_github_instance = MagicMock()
    mock_github_class.return_value = mock_github_instance
    
    # Attempt to initialize with wrong repo
    wrong_repo = "some-other-org/some-other-repo"
    GitHubIssueTaskService(repo_name=wrong_repo)
    
    # Verify it *correctly* scoped to the wrong repo (confirming our initialization logic uses what it is told)
    mock_github_instance.get_repo.assert_called_once_with(wrong_repo)
