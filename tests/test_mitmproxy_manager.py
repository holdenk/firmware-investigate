"""Tests for the mitmproxy manager module."""

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
