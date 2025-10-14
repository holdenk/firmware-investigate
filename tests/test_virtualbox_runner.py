"""Tests for the VirtualBox runner module."""

import pytest
from firmware_investigate.virtualbox_runner import VirtualBoxRunner


def test_virtualbox_runner_initialization():
    """Test VirtualBoxRunner initialization."""
    runner = VirtualBoxRunner(vm_name="test-vm")
    assert runner.vm_name == "test-vm"
    assert runner.proxy_host == "127.0.0.1"
    assert runner.proxy_port == 8080


def test_virtualbox_runner_custom_proxy():
    """Test VirtualBoxRunner with custom proxy settings."""
    runner = VirtualBoxRunner(
        vm_name="test-vm",
        proxy_host="192.168.1.1",
        proxy_port=9090,
    )
    assert runner.vm_name == "test-vm"
    assert runner.proxy_host == "192.168.1.1"
    assert runner.proxy_port == 9090


def test_virtualbox_runner_default_vm_name():
    """Test VirtualBoxRunner with default VM name."""
    runner = VirtualBoxRunner()
    assert runner.vm_name == "firmware-investigate-vm"


def test_virtualbox_runner_check_installation():
    """Test VirtualBox installation check."""
    runner = VirtualBoxRunner()

    # This will return True or False depending on whether VirtualBox is installed
    result = runner.check_virtualbox_installed()
    assert isinstance(result, bool)


def test_virtualbox_runner_check_vm_exists():
    """Test VM existence check."""
    runner = VirtualBoxRunner(vm_name="nonexistent-vm")

    # This should return False for a nonexistent VM
    result = runner.check_vm_exists()
    assert isinstance(result, bool)


def test_virtualbox_runner_run_missing_file(tmp_path):
    """Test running non-existent executable."""
    runner = VirtualBoxRunner(vm_name="test-vm")
    missing_exe = tmp_path / "missing.exe"

    if not runner.check_virtualbox_installed():
        # If VirtualBox is not installed, expect RuntimeError
        with pytest.raises(RuntimeError, match="VirtualBox is not installed"):
            runner.run(missing_exe)
    else:
        # If VirtualBox is installed, expect FileNotFoundError
        with pytest.raises(FileNotFoundError):
            runner.run(missing_exe)


def test_virtualbox_runner_attach_usb_device():
    """Test USB device attachment logic."""
    runner = VirtualBoxRunner(vm_name="test-vm")

    # Test with a fake device
    # This will fail if VirtualBox is not installed or VM doesn't exist,
    # but should not raise an exception
    result = runner.attach_usb_device("0x2685", "0x0900")
    assert isinstance(result, bool)
