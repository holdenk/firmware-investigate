"""USB Gadget device faker for Sena and Cardo devices."""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


class USBDeviceConfig:
    """Configuration for a USB device."""

    def __init__(
        self,
        vendor_id: str,
        product_id: str,
        manufacturer: str,
        product: str,
        serial: str = "123456",
    ):
        """Initialize USB device configuration.

        Args:
            vendor_id: USB vendor ID (e.g., "0x0003")
            product_id: USB product ID (e.g., "0x092b")
            manufacturer: Manufacturer string
            product: Product string
            serial: Serial number string
        """
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.manufacturer = manufacturer
        self.product = product
        self.serial = serial


# Device configurations
SENA_DEVICE = USBDeviceConfig(
    vendor_id="0x0003",
    product_id="0x092b",
    manufacturer="Sena Technologies",
    product="Sena Bluetooth Device",
    serial="SENA123456",
)

CARDO_DEVICE = USBDeviceConfig(
    vendor_id="0x2685",
    product_id="0x0900",
    manufacturer="Cardo Systems",
    product="Cardo Bluetooth Device",
    serial="CARDO123456",
)


class USBGadgetFaker:
    """Create fake USB devices using Linux USB gadget API."""

    CONFIGFS_PATH = Path("/sys/kernel/config/usb_gadget")

    def __init__(self):
        """Initialize USB gadget faker."""
        self.gadgets_created: List[str] = []

    def is_configfs_available(self) -> bool:
        """Check if USB gadget configfs is available.

        Returns:
            True if configfs is mounted and available, False otherwise.
        """
        return self.CONFIGFS_PATH.exists() and self.CONFIGFS_PATH.is_dir()

    def check_device_present(self, vendor_id: str, product_id: str) -> bool:
        """Check if a USB device with given vendor and product ID is present.

        Args:
            vendor_id: Vendor ID in format "0x0003" or "0003"
            product_id: Product ID in format "0x092b" or "092b"

        Returns:
            True if device is present, False otherwise.
        """
        # Normalize IDs (remove 0x prefix if present)
        vid = vendor_id.lower().replace("0x", "")
        pid = product_id.lower().replace("0x", "")

        try:
            result = subprocess.run(["lsusb"], capture_output=True, text=True, check=False)
            output = result.stdout.lower()

            # lsusb format: "Bus 001 Device 002: ID 0003:092b ..."
            device_id = f"{vid}:{pid}"
            return device_id in output

        except FileNotFoundError:
            # lsusb not available, assume device not present
            return False

    def get_available_udc(self) -> Optional[str]:
        """Get the first available USB device controller.

        Returns:
            Name of the UDC, or None if none available.
        """
        udc_path = Path("/sys/class/udc")
        if not udc_path.exists():
            return None

        udcs = list(udc_path.iterdir())
        if udcs:
            return udcs[0].name
        return None

    def create_gadget(self, device: USBDeviceConfig, gadget_name: str) -> bool:
        """Create a USB gadget device.

        Args:
            device: Device configuration
            gadget_name: Name for the gadget (e.g., "sena_fake")

        Returns:
            True if gadget was created successfully, False otherwise.
        """
        if not self.is_configfs_available():
            print(
                "ERROR: USB gadget configfs not available at " f"{self.CONFIGFS_PATH}",
                file=sys.stderr,
            )
            print(
                "Ensure configfs is mounted and the system supports USB gadgets.",
                file=sys.stderr,
            )
            return False

        gadget_path = self.CONFIGFS_PATH / gadget_name

        # Check if gadget already exists
        if gadget_path.exists():
            print(f"Gadget {gadget_name} already exists at {gadget_path}")
            return True

        try:
            # Create the gadget directory
            gadget_path.mkdir(parents=True, exist_ok=True)

            # Set USB device descriptor
            (gadget_path / "idVendor").write_text(device.vendor_id + "\n")
            (gadget_path / "idProduct").write_text(device.product_id + "\n")
            (gadget_path / "bcdDevice").write_text("0x0100\n")  # Device release 1.0
            (gadget_path / "bcdUSB").write_text("0x0200\n")  # USB 2.0

            # Create strings directory
            strings_path = gadget_path / "strings" / "0x409"  # English (US)
            strings_path.mkdir(parents=True, exist_ok=True)

            (strings_path / "manufacturer").write_text(device.manufacturer + "\n")
            (strings_path / "product").write_text(device.product + "\n")
            (strings_path / "serialnumber").write_text(device.serial + "\n")

            # Create configuration
            config_path = gadget_path / "configs" / "c.1"
            config_path.mkdir(parents=True, exist_ok=True)

            config_strings_path = config_path / "strings" / "0x409"
            config_strings_path.mkdir(parents=True, exist_ok=True)
            (config_strings_path / "configuration").write_text(f"{device.product} Configuration\n")

            # Set max power (in 2mA units, so 250 = 500mA)
            (config_path / "MaxPower").write_text("250\n")

            # Get available UDC and bind gadget
            udc = self.get_available_udc()
            if udc:
                (gadget_path / "UDC").write_text(udc + "\n")
                print(f"Successfully created and bound gadget {gadget_name} to {udc}")
            else:
                print(
                    f"WARNING: Created gadget {gadget_name} but no UDC available to bind",
                    file=sys.stderr,
                )
                print(
                    "You may need to load a UDC driver (e.g., dummy_hcd for testing)",
                    file=sys.stderr,
                )

            self.gadgets_created.append(gadget_name)
            return True

        except PermissionError:
            print(
                f"ERROR: Permission denied creating gadget {gadget_name}",
                file=sys.stderr,
            )
            print(
                "This operation requires root privileges. Try running with sudo.",
                file=sys.stderr,
            )
            return False
        except Exception as e:
            print(f"ERROR: Failed to create gadget {gadget_name}: {e}", file=sys.stderr)
            return False

    def remove_gadget(self, gadget_name: str) -> bool:
        """Remove a USB gadget device.

        Args:
            gadget_name: Name of the gadget to remove

        Returns:
            True if gadget was removed successfully, False otherwise.
        """
        gadget_path = self.CONFIGFS_PATH / gadget_name

        if not gadget_path.exists():
            print(f"Gadget {gadget_name} does not exist")
            return True

        try:
            # Unbind from UDC
            udc_file = gadget_path / "UDC"
            if udc_file.exists():
                udc_file.write_text("\n")

            # Remove configuration strings
            config_strings = gadget_path / "configs" / "c.1" / "strings" / "0x409"
            if config_strings.exists():
                config_strings.rmdir()

            # Remove configuration
            config_path = gadget_path / "configs" / "c.1"
            if config_path.exists():
                config_path.rmdir()

            # Remove strings
            strings_path = gadget_path / "strings" / "0x409"
            if strings_path.exists():
                strings_path.rmdir()

            # Remove gadget directory
            gadget_path.rmdir()

            print(f"Successfully removed gadget {gadget_name}")
            if gadget_name in self.gadgets_created:
                self.gadgets_created.remove(gadget_name)
            return True

        except PermissionError:
            print(
                f"ERROR: Permission denied removing gadget {gadget_name}",
                file=sys.stderr,
            )
            return False
        except Exception as e:
            print(f"ERROR: Failed to remove gadget {gadget_name}: {e}", file=sys.stderr)
            return False

    def setup_fake_devices(self, check_existing: bool = True) -> Dict[str, bool]:
        """Set up fake Sena and Cardo devices if they are not present.

        Args:
            check_existing: If True, only create devices that are not already present

        Returns:
            Dictionary with device names as keys and success status as values.
        """
        results = {}

        # Check and create Sena device
        sena_present = (
            self.check_device_present(SENA_DEVICE.vendor_id, SENA_DEVICE.product_id)
            if check_existing
            else False
        )

        if sena_present:
            print(
                f"Sena device ({SENA_DEVICE.vendor_id}:{SENA_DEVICE.product_id}) "
                "already present, skipping."
            )
            results["sena"] = True
        else:
            print(
                f"Sena device ({SENA_DEVICE.vendor_id}:{SENA_DEVICE.product_id}) "
                "not found, creating fake device..."
            )
            results["sena"] = self.create_gadget(SENA_DEVICE, "sena_fake")

        # Check and create Cardo device
        cardo_present = (
            self.check_device_present(CARDO_DEVICE.vendor_id, CARDO_DEVICE.product_id)
            if check_existing
            else False
        )

        if cardo_present:
            print(
                f"Cardo device ({CARDO_DEVICE.vendor_id}:{CARDO_DEVICE.product_id}) "
                "already present, skipping."
            )
            results["cardo"] = True
        else:
            print(
                f"Cardo device ({CARDO_DEVICE.vendor_id}:{CARDO_DEVICE.product_id}) "
                "not found, creating fake device..."
            )
            results["cardo"] = self.create_gadget(CARDO_DEVICE, "cardo_fake")

        return results

    def cleanup(self) -> None:
        """Clean up all gadgets created by this instance."""
        for gadget_name in self.gadgets_created[:]:  # Copy list to iterate safely
            self.remove_gadget(gadget_name)


def main():
    """Main entry point for USB gadget faker CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create fake USB devices for Sena and Cardo using Linux USB gadgets"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Create fake devices even if real devices are present",
    )

    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Remove all fake gadgets instead of creating them",
    )

    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check for device presence without creating gadgets",
    )

    args = parser.parse_args()

    faker = USBGadgetFaker()

    # Check if running as root
    if os.geteuid() != 0 and not args.check_only:
        print(
            "WARNING: Not running as root. Creating USB gadgets requires root privileges.",
            file=sys.stderr,
        )
        print(
            "Try running with: sudo python -m firmware_investigate.usb_gadget",
            file=sys.stderr,
        )

    if args.cleanup:
        faker.remove_gadget("sena_fake")
        faker.remove_gadget("cardo_fake")
        return 0

    if args.check_only:
        print("Checking for USB devices...")
        sena_present = faker.check_device_present(SENA_DEVICE.vendor_id, SENA_DEVICE.product_id)
        cardo_present = faker.check_device_present(CARDO_DEVICE.vendor_id, CARDO_DEVICE.product_id)

        print(
            f"Sena ({SENA_DEVICE.vendor_id}:{SENA_DEVICE.product_id}): "
            f"{'PRESENT' if sena_present else 'NOT FOUND'}"
        )
        print(
            f"Cardo ({CARDO_DEVICE.vendor_id}:{CARDO_DEVICE.product_id}): "
            f"{'PRESENT' if cardo_present else 'NOT FOUND'}"
        )
        return 0

    # Create fake devices
    print("USB Gadget Faker - Creating fake devices if needed")
    print("-" * 60)

    results = faker.setup_fake_devices(check_existing=not args.force)

    print("\n" + "-" * 60)
    print("Summary:")
    all_success = all(results.values())
    for device, success in results.items():
        status = "✓ OK" if success else "✗ FAILED"
        print(f"  {device.capitalize()}: {status}")

    if all_success:
        print("\nYou can verify the devices with: lsusb | grep -E '0003:092b|2685:0900'")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
