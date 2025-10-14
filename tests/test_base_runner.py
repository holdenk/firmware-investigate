"""Tests for the base runner module."""

from firmware_investigate.base_runner import BaseRunner
from pathlib import Path
from typing import Dict, List, Optional
import subprocess


class ConcreteRunner(BaseRunner):
    """Concrete implementation of BaseRunner for testing."""

    def run(
        self,
        executable: Path,
        args: Optional[List[str]] = None,
        usb_devices: Optional[List[Dict[str, str]]] = None,
    ) -> subprocess.CompletedProcess:
        """Test run implementation."""
        return subprocess.CompletedProcess(
            args=[str(executable)],
            returncode=0,
            stdout="test output",
            stderr="",
        )


def test_base_runner_initialization():
    """Test BaseRunner initialization."""
    runner = ConcreteRunner()
    assert runner.proxy_host == "127.0.0.1"
    assert runner.proxy_port == 8080


def test_base_runner_custom_proxy():
    """Test BaseRunner with custom proxy settings."""
    runner = ConcreteRunner(proxy_host="192.168.1.1", proxy_port=9090)
    assert runner.proxy_host == "192.168.1.1"
    assert runner.proxy_port == 9090


def test_base_runner_run_implementation(tmp_path):
    """Test that subclass can implement run method."""
    runner = ConcreteRunner()
    test_file = tmp_path / "test.exe"
    test_file.write_text("test")

    result = runner.run(test_file)
    assert result.returncode == 0
    assert result.stdout == "test output"
