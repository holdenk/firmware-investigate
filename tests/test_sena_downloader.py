"""Tests for Sena downloader."""

import tempfile
from pathlib import Path

from firmware_investigate.downloaders.sena import SenaDownloader


def test_sena_downloader_url():
    """Test that Sena downloader returns correct URL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = SenaDownloader(working_dir=tmpdir)
        assert downloader.get_url() == SenaDownloader.SENA_URL


def test_sena_downloader_filename():
    """Test that Sena downloader returns correct filename."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = SenaDownloader(working_dir=tmpdir)
        assert downloader.get_filename() == SenaDownloader.SENA_FILENAME


def test_sena_downloader_filepath():
    """Test that Sena downloader generates correct filepath."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = SenaDownloader(working_dir=tmpdir)
        expected_path = Path(tmpdir) / SenaDownloader.SENA_FILENAME
        assert downloader.get_filepath() == expected_path
