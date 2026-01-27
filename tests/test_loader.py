"""Tests for the loader module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from requests.exceptions import Timeout, ConnectionError, HTTPError
from langchain_core.documents import Document

from loader import load_star_wars_script, load_and_split_scripts


class TestLoadStarWarsScript:
    """Tests for load_star_wars_script function."""

    @patch('loader.requests.get')
    def test_successful_load(self, mock_get):
        """Test successful script loading."""
        mock_response = Mock()
        mock_response.content = b'<html><pre>LUKE: Hello there!</pre></html>'
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = load_star_wars_script(
            "http://example.com/script.html",
            "Test Movie"
        )

        assert isinstance(result, Document)
        assert result.page_content == "LUKE: Hello there!"
        assert result.metadata["title"] == "Test Movie"

    @patch('loader.requests.get')
    def test_missing_pre_tag_raises_value_error(self, mock_get):
        """Test that missing <pre> tag raises ValueError."""
        mock_response = Mock()
        mock_response.content = b'<html><div>No script here</div></html>'
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="No <pre> tag found"):
            load_star_wars_script(
                "http://example.com/script.html",
                "Test Movie"
            )

    @patch('loader.time.sleep')
    @patch('loader.requests.get')
    def test_retry_on_timeout(self, mock_get, mock_sleep):
        """Test that timeouts trigger retries."""
        mock_response = Mock()
        mock_response.content = b'<html><pre>Script content</pre></html>'
        mock_response.raise_for_status = Mock()
        
        # First two calls timeout, third succeeds
        mock_get.side_effect = [
            Timeout("Connection timed out"),
            Timeout("Connection timed out"),
            mock_response
        ]

        console = Mock()
        result = load_star_wars_script(
            "http://example.com/script.html",
            "Test Movie",
            console
        )

        assert result.page_content == "Script content"
        assert mock_get.call_count == 3

    @patch('loader.time.sleep')
    @patch('loader.requests.get')
    def test_all_retries_exhausted(self, mock_get, mock_sleep):
        """Test that RuntimeError is raised after all retries fail."""
        mock_get.side_effect = ConnectionError("Network error")

        console = Mock()
        with pytest.raises(RuntimeError, match="Failed to load script"):
            load_star_wars_script(
                "http://example.com/script.html",
                "Test Movie",
                console
            )

        # Should have tried MAX_RETRIES times (3)
        assert mock_get.call_count == 3

    @patch('loader.requests.get')
    def test_http_4xx_error_no_retry(self, mock_get):
        """Test that 4xx errors don't retry."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        console = Mock()
        with pytest.raises(HTTPError):
            load_star_wars_script(
                "http://example.com/script.html",
                "Test Movie",
                console
            )

        # Should only try once for 4xx errors
        assert mock_get.call_count == 1


class TestLoadAndSplitScripts:
    """Tests for load_and_split_scripts function."""

    @patch('loader.load_star_wars_script')
    def test_splits_scripts_into_chunks(self, mock_load_script):
        """Test that scripts are loaded and split into chunks."""
        # Create a mock document with enough content to split
        long_content = "SCENE 1\n\n" + "A" * 3000 + "\n\nSCENE 2\n\n" + "B" * 3000
        mock_load_script.return_value = Document(
            page_content=long_content,
            metadata={"title": "Test Movie"}
        )

        console = Mock()
        # Mock the Progress context manager
        with patch('loader.Progress') as mock_progress:
            mock_progress.return_value.__enter__ = Mock(return_value=Mock(
                add_task=Mock(return_value=1),
                update=Mock(),
                advance=Mock()
            ))
            mock_progress.return_value.__exit__ = Mock(return_value=False)
            
            result = load_and_split_scripts(console)

        assert len(result) > 0
        assert all(isinstance(doc, Document) for doc in result)
