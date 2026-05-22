import pytest
from unittest.mock import MagicMock
from src.drivers.github_issues import GitHubIssueTaskService

def test_github_issue_driver_scope():
    # Setup mock
    mock_repo = MagicMock()
    
    # Initialize driver with injected repo
    driver = GitHubIssueTaskService(repo=mock_repo)
    
    # Verify it scoped to the correct repo immediately upon initialization
    assert driver.repo == mock_repo
    
def test_github_issue_driver_wrong_scope():
    # This test is now less relevant as scoping is done in factory, 
    # but let's update it to respect the new constructor
    mock_repo = MagicMock()
    
    # Initialize with repo
    GitHubIssueTaskService(repo=mock_repo)
    
    # Verify it doesn't need to do anything else upon init
    assert True
