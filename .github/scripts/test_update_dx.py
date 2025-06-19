import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from datetime import datetime

# Mock the entire requests module before importing the script
sys.modules["requests"] = MagicMock()


# Patch environment variable, requests.get, and open
@patch.dict(os.environ, {"GH_TOKEN": "fake-token"})
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="# 📊 Developer Experience Metrics\nOld content...",
)
def test_update_dx_metrics(mock_file):
    # Mock PRs returned by the first API call
    mock_prs = [
        {
            "merged_at": "2024-06-01T12:00:00Z",
            "created_at": "2024-06-01T10:00:00Z",
            "url": "https://api.github.com/repos/owner/repo/pulls/1",
            "_links": {
                "review_comments": {
                    "href": "https://api.github.com/repos/owner/repo/pulls/1/comments"
                }
            },
        },
        {
            "merged_at": "2024-06-02T15:00:00Z",
            "created_at": "2024-06-02T12:00:00Z",
            "url": "https://api.github.com/repos/owner/repo/pulls/2",
            "_links": {
                "review_comments": {
                    "href": "https://api.github.com/repos/owner/repo/pulls/2/comments"
                }
            },
        },
    ]
    # Mock PR details (additions, deletions)
    pr_details = [
        {"additions": 10, "deletions": 5},
        {"additions": 20, "deletions": 10},
    ]
    # Mock review comments
    review_comments = [
        [{"created_at": "2024-06-01T10:30:00Z"}],  # First PR reviewed
        [],  # Second PR unreviewed
    ]

    # Setup mock requests
    with patch("requests.get") as mock_requests_get:

        def side_effect(url, headers=None, timeout=None):
            mock_resp = MagicMock()
            if "pulls?state=closed" in url:
                mock_resp.json.return_value = mock_prs
            elif url.endswith("/pulls/1"):
                mock_resp.json.return_value = pr_details[0]
            elif url.endswith("/pulls/2"):
                mock_resp.json.return_value = pr_details[1]
            elif url.endswith("/pulls/1/comments"):
                mock_resp.json.return_value = review_comments[0]
            elif url.endswith("/pulls/2/comments"):
                mock_resp.json.return_value = review_comments[1]
            else:
                raise ValueError(f"Unexpected URL: {url}")
            return mock_resp

        mock_requests_get.side_effect = side_effect

        # Patch datetime to return a fixed date
        with patch("datetime.datetime") as mock_datetime:
            # Mock datetime.now() to return a fixed datetime
            mock_now = MagicMock()
            mock_now.strftime.return_value = "2024-06-10"
            mock_datetime.now.return_value = mock_now

            # Mock datetime.fromisoformat to handle the string parsing
            def mock_fromisoformat(date_str):
                # Remove the 'Z' suffix and parse
                clean_str = date_str.rstrip("Z")
                return datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%S")

            mock_datetime.fromisoformat.side_effect = mock_fromisoformat

            # Import and run the script
            import importlib.util

            script_path = ".github/scripts/update_dx.py"
            spec = importlib.util.spec_from_file_location("update_dx", script_path)
            update_dx = importlib.util.module_from_spec(spec)
            sys.modules["update_dx"] = update_dx
            spec.loader.exec_module(update_dx)

    # Check that open was called for reading and writing
    assert mock_file.call_count >= 2
    # Check that the README was written with updated metrics
    written = "".join(call.args[0] for call in mock_file().write.call_args_list)
    assert "Avg PR Size" in written
    assert "2024-06-10" in written
    assert "% Merged Without Review" in written


@patch("builtins.open", new_callable=mock_open, read_data="No marker here")
def test_update_dx_marker_not_found(mock_file):
    # Patch requests.get to return one merged PR to avoid division by zero
    with patch("requests.get") as mock_requests_get:
        # Return one merged PR
        mock_prs = [
            {
                "merged_at": "2024-06-01T12:00:00Z",
                "created_at": "2024-06-01T10:00:00Z",
                "url": "https://api.github.com/repos/owner/repo/pulls/1",
                "_links": {
                    "review_comments": {
                        "href": "https://api.github.com/repos/owner/repo/pulls/1/comments"
                    }
                },
            }
        ]

        def side_effect(url, headers=None, timeout=None):
            mock_resp = MagicMock()
            if "pulls?state=closed" in url:
                mock_resp.json.return_value = mock_prs
            elif url.endswith("/pulls/1"):
                mock_resp.json.return_value = {"additions": 10, "deletions": 5}
            elif url.endswith("/pulls/1/comments"):
                mock_resp.json.return_value = []
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        mock_requests_get.side_effect = side_effect

        # Patch datetime to avoid issues
        with patch("datetime.datetime") as mock_datetime:
            mock_now = MagicMock()
            mock_now.strftime.return_value = "2024-06-10"
            mock_datetime.now.return_value = mock_now

            def mock_fromisoformat(date_str):
                clean_str = date_str.rstrip("Z")
                return datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%S")

            mock_datetime.fromisoformat.side_effect = mock_fromisoformat

            # Patch print to capture output
            with patch("builtins.print") as mock_print:
                import importlib.util

                script_path = ".github/scripts/update_dx.py"
                spec = importlib.util.spec_from_file_location("update_dx", script_path)
                update_dx = importlib.util.module_from_spec(spec)
                sys.modules["update_dx"] = update_dx
                spec.loader.exec_module(update_dx)
                # Check that the marker not found message was printed
                mock_print.assert_any_call("Marker not found in README.md")
