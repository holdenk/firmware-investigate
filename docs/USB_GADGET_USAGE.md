# USB Gadget Faker Usage Examples

This document provides detailed examples of using the USB gadget faker functionality.

## Basic Usage

### Check if devices are present

Using the main CLI:
```bash
firmware-investigate --check-usb-devices
```

Using the standalone module:
```bash
python -m firmware_investigate.usb_gadget --check-only
```

### Create fake devices

**Note: Requires root privileges and Linux with USB gadget support**

Using the main CLI:
```bash
sudo firmware-investigate --setup-usb-gadgets
```

Using the standalone module:
```bash
sudo python -m firmware_investigate.usb_gadget
```

### Force creation (even if real devices are present)

```bash
sudo python -m firmware_investigate.usb_gadget --force
```

### Clean up fake devices

```bash
sudo python -m firmware_investigate.usb_gadget --cleanup
```

## Python API Usage

### Check for device presence

```python
from firmware_investigate import USBGadgetFaker

faker = USBGadgetFaker()

# Check individual devices
sena_present = faker.check_device_present("0x0003", "0x092b")
cardo_present = faker.check_device_present("0x2685", "0x0900")

print(f"Sena device present: {sena_present}")
print(f"Cardo device present: {cardo_present}")
```

### Create fake devices programmatically

```python
from firmware_investigate import USBGadgetFaker

# Create faker instance
faker = USBGadgetFaker()

# Setup fake devices (only if not already present)
results = faker.setup_fake_devices(check_existing=True)

# Check results
for device, success in results.items():
    print(f"{device}: {'OK' if success else 'FAILED'}")

# Clean up when done
faker.cleanup()
```

### Access device configurations

```python
from firmware_investigate import SENA_DEVICE, CARDO_DEVICE

print(f"Sena Device: {SENA_DEVICE.vendor_id}:{SENA_DEVICE.product_id}")
print(f"  Manufacturer: {SENA_DEVICE.manufacturer}")
print(f"  Product: {SENA_DEVICE.product}")
print(f"  Serial: {SENA_DEVICE.serial}")

print(f"\nCardo Device: {CARDO_DEVICE.vendor_id}:{CARDO_DEVICE.product_id}")
print(f"  Manufacturer: {CARDO_DEVICE.manufacturer}")
print(f"  Product: {CARDO_DEVICE.product}")
print(f"  Serial: {CARDO_DEVICE.serial}")
```

## System Requirements

### Prerequisites

1. **Linux operating system** with USB gadget support
2. **ConfigFS mounted** at `/sys/kernel/config/usb_gadget`
3. **USB Device Controller (UDC)** available
4. **Root privileges** for creating gadget devices

### Setting up USB Gadget Support (for testing)

If you're testing in a development environment without physical USB gadget hardware:

1. Load the dummy_hcd kernel module:
   ```bash
   sudo modprobe dummy_hcd
   ```

2. Mount configfs (if not already mounted):
   ```bash
   sudo mount -t configfs none /sys/kernel/config
   ```

3. Verify UDC is available:
   ```bash
   ls /sys/class/udc/
   ```

## Verifying Created Devices

After creating fake devices, verify they appear in lsusb:

```bash
# Show all USB devices
lsusb

# Filter for Sena and Cardo devices
lsusb | grep -E '0003:092b|2685:0900'
```

Example output:
```
Bus 001 Device 002: ID 0003:092b Sena Technologies Sena Bluetooth Device
Bus 001 Device 003: ID 2685:0900 Cardo Systems Cardo Bluetooth Device
```

## Troubleshooting

### "USB gadget configfs not available"

This error means the system doesn't have USB gadget support or configfs is not mounted.

Solutions:
- Ensure you're running on a Linux system
- Check if configfs is mounted: `mount | grep configfs`
- Try loading dummy_hcd: `sudo modprobe dummy_hcd`

### "Permission denied"

USB gadget creation requires root privileges.

Solution:
- Run with sudo: `sudo python -m firmware_investigate.usb_gadget`

### "No UDC available"

No USB Device Controller is available on the system.

Solutions:
- Load the dummy_hcd module: `sudo modprobe dummy_hcd`
- Check available UDCs: `ls /sys/class/udc/`
- On Raspberry Pi or similar boards, check if dwc2 or other UDC drivers are loaded

## Use Cases

### Testing Firmware Updaters

The USB gadget faker allows you to test firmware updater applications without physical hardware:

1. Create fake USB devices
2. Run the firmware updater application
3. Observe how it detects and interacts with the fake devices
4. Clean up fake devices when testing is complete

### Continuous Integration

In CI/CD pipelines, you can:
- Check if devices are present (should be absent in CI)
- Document expected device IDs
- Test device detection logic without hardware

### Development and Debugging

During development:
- Test USB device enumeration code
- Verify device ID matching logic
- Debug firmware update workflows
