"""Tests for the update_dx.py script."""

import os
from datetime import datetime, timedelta
from unittest.mock import patch, mock_open
import pytest
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.update_dx import TOKEN, REPO, update_metrics

@pytest.fixture(autouse=True)
def mock_env():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {'GH_TOKEN': 'fake-token-for-testing'}):
        yield

@pytest.fixture
def mock_pr_response():
    """Mock response for pull requests API."""
    return [
        {
            "url": "https://api.github.com/repos/test/test/pulls/1",
            "created_at": "2024-01-01T10:00:00Z",
            "merged_at": "2024-01-01T12:00:00Z",
            "_links": {
                "review_comments": {
                    "href": "https://api.github.com/repos/test/test/pulls/1/comments"
                }
            }
        }
    ]

@pytest.fixture
def mock_pr_details():
    """Mock response for pull request details."""
    return {
        "additions": 100,
        "deletions": 50
    }

@pytest.fixture
def mock_reviews():
    """Mock response for review comments."""
    return [
        {
            "created_at": "2024-01-01T11:00:00Z"
        }
    ]

def test_token_exists():
    """Test that GitHub token is properly configured."""
    assert TOKEN is not None, "GitHub token should be set"
    assert REPO is not None, "Repository should be set"

@patch('requests.get')
def test_pr_processing(mock_get, mock_pr_response, mock_pr_details, mock_reviews):
    """Test processing of pull request data."""
    # Mock API responses
    mock_get.side_effect = [
        type('Response', (), {'json': lambda: mock_pr_response})(),
        type('Response', (), {'json': lambda: mock_pr_details})(),
        type('Response', (), {'json': lambda: mock_reviews})()
    ]

    # Mock file operations
    mock_readme = """# Some content
    # 📊 Developer Experience Metrics
    Old metrics
    # More content"""
    
    with patch('builtins.open', mock_open(read_data=mock_readme)):
        metrics = update_metrics()
        
        assert "Avg PR Size" in metrics
        assert "150 LOC" in metrics  # 100 additions + 50 deletions
        assert "1.0 hours" in metrics  # Time from creation to first review
        assert "2.0 hours" in metrics  # Time from creation to merge

@patch('requests.get')
def test_error_handling(mock_get):
    """Test handling of API errors."""
    mock_get.return_value = type('Response', (), {'json': lambda: {"message": "API Error"}})()
    
    with pytest.raises(SystemExit):
        update_metrics() 