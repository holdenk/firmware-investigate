"""Tests for Motorola downloader."""

import tempfile
from pathlib import Path

from firmware_investigate.downloaders.motorola import MotorolaDownloader


def test_motorola_downloader_url():
    """Test that Motorola downloader returns correct APK URL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir)
        assert downloader.get_url() == MotorolaDownloader.MOTOROLA_APK_URL


def test_motorola_downloader_url_windows():
    """Test that Motorola downloader returns APK URL even on Windows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="windows")
        # APKs are platform-agnostic, so URL is the same
        assert downloader.get_url() == MotorolaDownloader.MOTOROLA_APK_URL


def test_motorola_downloader_url_macos():
    """Test that Motorola downloader returns APK URL even on macOS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="darwin")
        # APKs are platform-agnostic, so URL is the same
        assert downloader.get_url() == MotorolaDownloader.MOTOROLA_APK_URL


def test_motorola_downloader_filename():
    """Test that Motorola downloader returns correct APK filename."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir)
        assert downloader.get_filename() == "bullitt_satellite_messenger.apk"


def test_motorola_downloader_filename_windows():
    """Test that Motorola downloader returns APK filename on Windows."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="windows")
        # APKs are platform-agnostic
        assert downloader.get_filename() == "bullitt_satellite_messenger.apk"


def test_motorola_downloader_filename_macos():
    """Test that Motorola downloader returns APK filename on macOS."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="darwin")
        # APKs are platform-agnostic
        assert downloader.get_filename() == "bullitt_satellite_messenger.apk"


def test_motorola_downloader_filepath():
    """Test that Motorola downloader generates correct filepath."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = MotorolaDownloader(working_dir=tmpdir, platform_override="windows")
        expected_path = Path(tmpdir) / "bullitt_satellite_messenger.apk"
        assert downloader.get_filepath() == expected_path
