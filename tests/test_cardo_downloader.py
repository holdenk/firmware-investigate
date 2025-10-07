"""Tests for Cardo downloader."""

import tempfile
from pathlib import Path

from firmware_investigate.downloaders.cardo import CardoDownloader


def test_cardo_downloader_url_windows():
    """Test that Cardo downloader returns correct URL for Windows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = CardoDownloader(working_dir=tmpdir, platform_override="windows")
        assert downloader.get_url() == CardoDownloader.CARDO_WINDOWS_URL


def test_cardo_downloader_url_macos():
    """Test that Cardo downloader returns correct URL for macOS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = CardoDownloader(working_dir=tmpdir, platform_override="darwin")
        assert downloader.get_url() == CardoDownloader.CARDO_MACOS_URL


def test_cardo_downloader_filename_windows():
    """Test that Cardo downloader returns correct filename for Windows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = CardoDownloader(working_dir=tmpdir, platform_override="windows")
        assert downloader.get_filename() == "cardo_updater_win_latest.exe"


def test_cardo_downloader_filename_macos():
    """Test that Cardo downloader returns correct filename for macOS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = CardoDownloader(working_dir=tmpdir, platform_override="darwin")
        assert downloader.get_filename() == "CardoUpdateLite_OTA_darwin_arm64_latest.dmg"


def test_cardo_downloader_filepath():
    """Test that Cardo downloader generates correct filepath."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = CardoDownloader(working_dir=tmpdir, platform_override="windows")
        expected_path = Path(tmpdir) / "cardo_updater_win_latest.exe"
        assert downloader.get_filepath() == expected_path
