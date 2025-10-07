"""Tests for Sena downloader."""

import tempfile
from pathlib import Path

from firmware_investigate.downloaders.sena import SenaDownloader


def test_sena_downloader_url_windows():
    """Test that Sena downloader returns correct URL for Windows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = SenaDownloader(working_dir=tmpdir, platform_override="windows")
        assert downloader.get_url() == SenaDownloader.SENA_WINDOWS_URL


def test_sena_downloader_url_macos():
    """Test that Sena downloader returns correct URL for macOS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = SenaDownloader(working_dir=tmpdir, platform_override="darwin")
        assert downloader.get_url() == SenaDownloader.SENA_MACOS_URL


def test_sena_downloader_filename_windows():
    """Test that Sena downloader returns correct filename for Windows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = SenaDownloader(working_dir=tmpdir, platform_override="windows")
        assert downloader.get_filename() == "SenaDeviceManagerForWindows-v4.4.16-setup_x64.exe"


def test_sena_downloader_filename_macos():
    """Test that Sena downloader returns correct filename for macOS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = SenaDownloader(working_dir=tmpdir, platform_override="darwin")
        assert downloader.get_filename() == "SENADeviceManagerForMAC-v4.4.16.pkg"


def test_sena_downloader_filepath():
    """Test that Sena downloader generates correct filepath."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = SenaDownloader(working_dir=tmpdir, platform_override="windows")
        expected_path = Path(tmpdir) / "SenaDeviceManagerForWindows-v4.4.16-setup_x64.exe"
        assert downloader.get_filepath() == expected_path
