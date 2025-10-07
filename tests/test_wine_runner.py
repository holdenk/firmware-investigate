"""Tests for the Wine runner module."""

import pytest
from pathlib import Path
from firmware_investigate.wine_runner import WineRunner


def test_wine_runner_initialization(tmp_path):
    """Test WineRunner initialization."""
    runner = WineRunner(wine_prefix=tmp_path / "wine_prefix")
    assert runner.wine_prefix == tmp_path / "wine_prefix"
    assert runner.proxy_host == "127.0.0.1"
    assert runner.proxy_port == 8080


def test_wine_runner_custom_proxy(tmp_path):
    """Test WineRunner with custom proxy settings."""
    runner = WineRunner(
        wine_prefix=tmp_path / "wine_prefix",
        proxy_host="192.168.1.1",
        proxy_port=9090,
    )
    assert runner.proxy_host == "192.168.1.1"
    assert runner.proxy_port == 9090


def test_wine_runner_setup_environment(tmp_path):
    """Test environment variable setup."""
    runner = WineRunner(wine_prefix=tmp_path / "wine_prefix")
    env = runner.setup_environment()
    
    assert "WINEPREFIX" in env
    assert env["WINEPREFIX"] == str(tmp_path / "wine_prefix")
    assert env["http_proxy"] == "http://127.0.0.1:8080"
    assert env["https_proxy"] == "http://127.0.0.1:8080"
    assert "WINEDEBUG" in env


def test_wine_runner_check_wine_installed():
    """Test Wine installation check."""
    runner = WineRunner()
    
    # This will return True or False depending on whether Wine is installed
    result = runner.check_wine_installed()
    assert isinstance(result, bool)


def test_wine_runner_run_missing_file(tmp_path):
    """Test running non-existent executable."""
    runner = WineRunner(wine_prefix=tmp_path / "wine_prefix")
    missing_exe = tmp_path / "missing.exe"
    
    if not runner.check_wine_installed():
        # If Wine is not installed, expect RuntimeError
        with pytest.raises(RuntimeError, match="Wine is not installed"):
            runner.run(missing_exe)
    else:
        # If Wine is installed, expect FileNotFoundError
        with pytest.raises(FileNotFoundError):
            runner.run(missing_exe)
