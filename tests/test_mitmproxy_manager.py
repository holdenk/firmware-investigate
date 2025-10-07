"""Tests for the mitmproxy manager module."""

import pytest
from pathlib import Path
from firmware_investigate.mitmproxy_manager import MitmproxyManager


def test_mitmproxy_manager_initialization(tmp_path):
    """Test MitmproxyManager initialization."""
    manager = MitmproxyManager(port=8080, output_dir=tmp_path / "mitm")
    assert manager.port == 8080
    assert manager.output_dir == tmp_path / "mitm"
    assert manager.mode == "regular"


def test_mitmproxy_manager_custom_port(tmp_path):
    """Test MitmproxyManager with custom port."""
    manager = MitmproxyManager(port=9090, output_dir=tmp_path / "mitm")
    assert manager.port == 9090


def test_mitmproxy_manager_check_installed():
    """Test mitmproxy installation check."""
    manager = MitmproxyManager()
    
    # This will return True or False depending on whether mitmproxy is installed
    result = manager.check_mitmproxy_installed()
    assert isinstance(result, bool)


def test_mitmproxy_manager_create_config_script(tmp_path):
    """Test addon script creation."""
    manager = MitmproxyManager(output_dir=tmp_path / "mitm")
    
    script_path = manager.create_config_script()
    
    assert script_path.exists()
    assert script_path.name == "firmware_addon.py"
    
    # Check script content
    content = script_path.read_text()
    assert "FirmwareAddon" in content
    assert "mitmproxy" in content
