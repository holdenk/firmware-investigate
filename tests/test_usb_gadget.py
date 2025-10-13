"""Tests for USB gadget faker."""

from unittest.mock import Mock, patch

from firmware_investigate.usb_gadget import (
    CARDO_DEVICE,
    SENA_DEVICE,
    USBDeviceConfig,
    USBGadgetFaker,
)


def test_usb_device_config():
    """Test USB device configuration initialization."""
    config = USBDeviceConfig(
        vendor_id="0x1234",
        product_id="0x5678",
        manufacturer="Test Manufacturer",
        product="Test Product",
        serial="TEST123",
    )

    assert config.vendor_id == "0x1234"
    assert config.product_id == "0x5678"
    assert config.manufacturer == "Test Manufacturer"
    assert config.product == "Test Product"
    assert config.serial == "TEST123"


def test_sena_device_config():
    """Test Sena device configuration."""
    assert SENA_DEVICE.vendor_id == "0x0003"
    assert SENA_DEVICE.product_id == "0x092b"
    assert "Sena" in SENA_DEVICE.manufacturer


def test_cardo_device_config():
    """Test Cardo device configuration."""
    assert CARDO_DEVICE.vendor_id == "0x2685"
    assert CARDO_DEVICE.product_id == "0x0900"
    assert "Cardo" in CARDO_DEVICE.manufacturer


def test_usb_gadget_faker_initialization():
    """Test USBGadgetFaker initialization."""
    faker = USBGadgetFaker()
    assert faker.gadgets_created == []


def test_is_configfs_available_false():
    """Test configfs availability check when not available."""
    faker = USBGadgetFaker()
    # In most test environments, configfs won't be available
    result = faker.is_configfs_available()
    # This will typically be False in test environment
    assert isinstance(result, bool)


def test_check_device_present_with_lsusb():
    """Test device presence check with mocked lsusb."""
    faker = USBGadgetFaker()

    # Mock lsusb output showing Sena device
    mock_result = Mock()
    mock_result.stdout = "Bus 001 Device 002: ID 0003:092b Sena Technologies"
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        assert faker.check_device_present("0x0003", "0x092b") is True
        assert faker.check_device_present("0003", "092b") is True
        assert faker.check_device_present("0x2685", "0x0900") is False


def test_check_device_present_without_lsusb():
    """Test device presence check when lsusb is not available."""
    faker = USBGadgetFaker()

    with patch("subprocess.run", side_effect=FileNotFoundError()):
        # Should return False when lsusb is not available
        assert faker.check_device_present("0x0003", "0x092b") is False


def test_check_device_present_case_insensitive():
    """Test that device check is case insensitive."""
    faker = USBGadgetFaker()

    mock_result = Mock()
    mock_result.stdout = "Bus 001 Device 002: ID 0003:092B Sena Technologies"
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        # Should match regardless of case
        assert faker.check_device_present("0x0003", "0x092b") is True
        assert faker.check_device_present("0x0003", "0x092B") is True


def test_get_available_udc_none():
    """Test get_available_udc when no UDC is available."""
    faker = USBGadgetFaker()
    # In most test environments, no UDC will be available
    result = faker.get_available_udc()
    # Should return None or a string
    assert result is None or isinstance(result, str)


@patch("pathlib.Path.exists")
@patch("pathlib.Path.is_dir")
def test_is_configfs_available_true(mock_is_dir, mock_exists):
    """Test configfs availability when it exists."""
    mock_exists.return_value = True
    mock_is_dir.return_value = True

    faker = USBGadgetFaker()
    assert faker.is_configfs_available() is True


def test_setup_fake_devices_no_configfs():
    """Test setup_fake_devices when configfs is not available."""
    faker = USBGadgetFaker()

    with patch.object(faker, "is_configfs_available", return_value=False):
        with patch.object(faker, "check_device_present", return_value=False):
            results = faker.setup_fake_devices()

            # Should attempt to create both devices
            assert "sena" in results
            assert "cardo" in results
            # Both should fail due to no configfs
            assert results["sena"] is False
            assert results["cardo"] is False


def test_setup_fake_devices_already_present():
    """Test setup_fake_devices when devices are already present."""
    faker = USBGadgetFaker()

    with patch.object(faker, "check_device_present", return_value=True):
        results = faker.setup_fake_devices()

        # Both devices should be reported as present
        assert results["sena"] is True
        assert results["cardo"] is True


def test_setup_fake_devices_partial_present():
    """Test setup_fake_devices when only one device is present."""
    faker = USBGadgetFaker()

    def mock_check(vid, pid):
        # Sena is present, Cardo is not
        if vid == "0x0003" and pid == "0x092b":
            return True
        return False

    with patch.object(faker, "check_device_present", side_effect=mock_check):
        with patch.object(faker, "is_configfs_available", return_value=False):
            results = faker.setup_fake_devices()

            # Sena should be reported as present
            assert results["sena"] is True
            # Cardo should fail (no configfs)
            assert results["cardo"] is False


def test_cleanup():
    """Test cleanup of created gadgets."""
    faker = USBGadgetFaker()
    faker.gadgets_created = ["test_gadget1", "test_gadget2"]

    with patch.object(faker, "remove_gadget", return_value=True) as mock_remove:
        faker.cleanup()

        # Should remove both gadgets
        assert mock_remove.call_count == 2
        mock_remove.assert_any_call("test_gadget1")
        mock_remove.assert_any_call("test_gadget2")
