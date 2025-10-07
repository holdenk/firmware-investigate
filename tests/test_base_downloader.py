"""Tests for base downloader functionality."""

import tempfile
from pathlib import Path

from firmware_investigate.downloaders.base import BaseDownloader


class MockDownloader(BaseDownloader):
    """Mock implementation of BaseDownloader."""

    def get_url(self) -> str:
        return "https://example.com/test.exe"

    def get_filename(self) -> str:
        return "test.exe"


def test_downloader_initialization():
    """Test that downloader initializes correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MockDownloader(working_dir=tmpdir)
        assert downloader.working_dir == Path(tmpdir)
        assert downloader.working_dir.exists()


def test_downloader_platform_override():
    """Test that platform override works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MockDownloader(working_dir=tmpdir, platform_override="windows")
        assert downloader.platform == "windows"


def test_get_filepath():
    """Test filepath generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MockDownloader(working_dir=tmpdir)
        filepath = downloader.get_filepath()
        assert filepath == Path(tmpdir) / "test.exe"


def test_file_exists():
    """Test file existence check."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MockDownloader(working_dir=tmpdir)

        # File doesn't exist initially
        assert not downloader.file_exists()

        # Create the file
        downloader.get_filepath().touch()

        # Now it exists
        assert downloader.file_exists()


def test_working_dir_creation():
    """Test that working directory is created if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        working_path = Path(tmpdir) / "subdir" / "working"
        MockDownloader(working_dir=str(working_path))
        assert working_path.exists()
