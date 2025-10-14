"""Tests for the macOS runner module."""

import platform
import pytest
from firmware_investigate.macos_runner import MacOSRunner


def test_macos_runner_initialization():
    """Test MacOSRunner initialization."""
    runner = MacOSRunner()
    assert runner.proxy_host == "127.0.0.1"
    assert runner.proxy_port == 8080


def test_macos_runner_custom_proxy():
    """Test MacOSRunner with custom proxy settings."""
    runner = MacOSRunner(proxy_host="192.168.1.1", proxy_port=9090)
    assert runner.proxy_host == "192.168.1.1"
    assert runner.proxy_port == 9090


def test_macos_runner_check_macos():
    """Test macOS detection."""
    runner = MacOSRunner()
    result = runner.check_macos()
    assert isinstance(result, bool)
    # Should return True only on macOS
    assert result == (platform.system() == "Darwin")


def test_macos_runner_run_missing_file(tmp_path):
    """Test running non-existent executable."""
    runner = MacOSRunner()
    missing_file = tmp_path / "missing.pkg"

    if not runner.check_macos():
        # If not on macOS, expect RuntimeError about platform
        with pytest.raises(RuntimeError, match="can only be used on macOS"):
            runner.run(missing_file)
    else:
        # If on macOS, expect FileNotFoundError
        with pytest.raises(FileNotFoundError):
            runner.run(missing_file)
