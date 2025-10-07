"""Tests for FCC lookup functionality."""

from firmware_investigate.fcc_lookup import (
    DeviceInfo,
    KNOWN_DEVICES,
    get_device_info,
    list_all_devices,
    print_device_info,
)


def test_known_devices_exist():
    """Test that known devices are defined."""
    assert len(KNOWN_DEVICES) > 0
    assert "sena_50s" in KNOWN_DEVICES
    assert "cardo_packtalk_bold" in KNOWN_DEVICES
    assert "motorola_defy_satellite" in KNOWN_DEVICES


def test_sena_50s_info():
    """Test Sena 50S device information."""
    device = get_device_info("sena_50s")
    assert device is not None
    assert device.name == "Sena 50S"
    assert device.fcc_id == "Q95ER19"
    assert device.manufacturer == "Sena Technologies"
    assert "fcc.report" in device.fcc_report_url


def test_cardo_packtalk_bold_info():
    """Test Cardo Packtalk Bold device information."""
    device = get_device_info("cardo_packtalk_bold")
    assert device is not None
    assert device.name == "Cardo Packtalk Bold"
    assert device.fcc_id == "UDO-DMCJBL"
    assert device.manufacturer == "Cardo Systems"
    assert "fcc.report" in device.fcc_report_url


def test_motorola_defy_satellite_info():
    """Test Motorola Defy Satellite device information."""
    device = get_device_info("motorola_defy_satellite")
    assert device is not None
    assert device.name == "Motorola Defy Satellite"
    assert device.fcc_id == "IHDT56WJ1"
    assert device.manufacturer == "Motorola Mobility (Lenovo)"
    assert "fcc.report" in device.fcc_report_url


def test_get_device_info_unknown():
    """Test getting info for unknown device."""
    device = get_device_info("unknown_device")
    assert device is None


def test_list_all_devices():
    """Test listing all known devices."""
    devices = list_all_devices()
    assert len(devices) == 3
    assert all(isinstance(d, DeviceInfo) for d in devices)


def test_device_info_dataclass():
    """Test DeviceInfo dataclass."""
    device = DeviceInfo(
        name="Test Device",
        fcc_id="TEST123",
        manufacturer="Test Manufacturer",
        fcc_report_url="https://fcc.report/FCC-ID/TEST123",
        notes="Test notes",
    )
    assert device.name == "Test Device"
    assert device.fcc_id == "TEST123"
    assert device.manufacturer == "Test Manufacturer"
    assert device.notes == "Test notes"


def test_print_device_info(capsys):
    """Test printing device information."""
    device = DeviceInfo(
        name="Test Device",
        fcc_id="TEST123",
        manufacturer="Test Manufacturer",
        fcc_report_url="https://fcc.report/FCC-ID/TEST123",
    )
    print_device_info(device)
    captured = capsys.readouterr()
    assert "Test Device" in captured.out
    assert "TEST123" in captured.out
    assert "Test Manufacturer" in captured.out
