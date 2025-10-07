"""Tests for Cardo downloader."""

import tempfile
from pathlib import Path

from firmware_investigate.downloaders.cardo import CardoDownloader


def test_cardo_downloader_url():
    """Test that Cardo downloader returns correct URL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = CardoDownloader(working_dir=tmpdir)
        assert downloader.get_url() == CardoDownloader.CARDO_URL


def test_cardo_downloader_filename():
    """Test that Cardo downloader returns correct filename."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = CardoDownloader(working_dir=tmpdir)
        assert downloader.get_filename() == CardoDownloader.CARDO_FILENAME


def test_cardo_downloader_filepath():
    """Test that Cardo downloader generates correct filepath."""
    with tempfile.TemporaryDirectory() as tmpdir:
        downloader = CardoDownloader(working_dir=tmpdir)
        expected_path = Path(tmpdir) / CardoDownloader.CARDO_FILENAME
        assert downloader.get_filepath() == expected_path
