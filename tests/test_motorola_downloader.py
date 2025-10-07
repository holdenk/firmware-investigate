"""Tests for Motorola downloader."""

import tempfile
from pathlib import Path

from firmware_investigate.downloaders.motorola import MotorolaDownloader


def test_motorola_downloader_url_windows():
    """Test that Motorola downloader returns correct URL for Windows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="windows")
        assert downloader.get_url() == MotorolaDownloader.MOTOROLA_WINDOWS_URL


def test_motorola_downloader_url_macos():
    """Test that Motorola downloader returns correct URL for macOS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="darwin")
        assert downloader.get_url() == MotorolaDownloader.MOTOROLA_MACOS_URL


def test_motorola_downloader_filename_windows():
    """Test that Motorola downloader returns correct filename for Windows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="windows")
        assert downloader.get_filename() == "MotDefySatelliteLinkManager_Setup.exe"


def test_motorola_downloader_filename_macos():
    """Test that Motorola downloader returns correct filename for macOS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="darwin")
        assert downloader.get_filename() == "MotDefySatelliteLinkManager.dmg"


def test_motorola_downloader_filepath():
    """Test that Motorola downloader generates correct filepath."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="windows")
        expected_path = Path(tmpdir) / "MotDefySatelliteLinkManager_Setup.exe"
        assert downloader.get_filepath() == expected_path
