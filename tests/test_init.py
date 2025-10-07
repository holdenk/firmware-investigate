"""Test package initialization."""

import firmware_investigate


def test_version():
    """Test that version is defined."""
    assert hasattr(firmware_investigate, "__version__")
    assert isinstance(firmware_investigate.__version__, str)
