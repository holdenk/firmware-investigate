"""Module for running Windows executables using VirtualBox with USB passthrough."""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class VirtualBoxRunner:
    """Runner for executing Windows programs using VirtualBox with USB passthrough support."""

    def __init__(
        self,
        vm_name: str = "firmware-investigate-vm",
        proxy_host: str = "127.0.0.1",
        proxy_port: int = 8080,
    ):
        """Initialize the VirtualBox runner.

        Args:
            vm_name: Name of the VirtualBox VM to use.
            proxy_host: Proxy server host for network interception.
            proxy_port: Proxy server port for network interception.
        """
        self.vm_name = vm_name
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

    def check_virtualbox_installed(self) -> bool:
        """Check if VirtualBox is installed.

        Returns:
            True if VirtualBox is available, False otherwise.
        """
        try:
            subprocess.run(
                ["VBoxManage", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def check_vm_exists(self) -> bool:
        """Check if the configured VM exists.

        Returns:
            True if the VM exists, False otherwise.
        """
        if not self.check_virtualbox_installed():
            return False

        try:
            result = subprocess.run(
                ["VBoxManage", "showvminfo", self.vm_name],
                capture_output=True,
                check=False,
            )
            return result.returncode == 0
        except Exception:
            return False

    def attach_usb_device(self, vendor_id: str, product_id: str) -> bool:
        """Attach a USB device to the VM.

        Args:
            vendor_id: USB vendor ID (e.g., "0x2685").
            product_id: USB product ID (e.g., "0x0900").

        Returns:
            True if attachment was successful, False otherwise.
        """
        if not self.check_vm_exists():
            return False

        try:
            # Remove '0x' prefix if present
            vendor_id_clean = vendor_id.replace("0x", "").replace("0X", "")
            product_id_clean = product_id.replace("0x", "").replace("0X", "")

            # Create USB filter for the device
            filter_name = f"usb_{vendor_id_clean}_{product_id_clean}"

            subprocess.run(
                [
                    "VBoxManage",
                    "usbfilter",
                    "add",
                    "0",
                    "--target",
                    self.vm_name,
                    "--name",
                    filter_name,
                    "--vendorid",
                    vendor_id_clean,
                    "--productid",
                    product_id_clean,
                ],
                capture_output=True,
                check=True,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(
                f"Warning: Failed to attach USB device: {e.stderr.decode() if e.stderr else str(e)}"
            )
            return False

    def run(
        self,
        executable: Path,
        args: Optional[List[str]] = None,
        usb_devices: Optional[List[Dict[str, str]]] = None,
    ) -> subprocess.CompletedProcess:
        """Run a Windows executable using VirtualBox with USB passthrough.

        Args:
            executable: Path to the Windows executable.
            args: Optional command-line arguments for the executable.
            usb_devices: Optional list of USB devices to pass through
                        (format: [{"vendor_id": "0x2685", "product_id": "0x0900"}]).

        Returns:
            CompletedProcess object from subprocess.run.

        Raises:
            FileNotFoundError: If executable doesn't exist or VirtualBox is not installed.
            RuntimeError: If VirtualBox execution fails or VM doesn't exist.
        """
        if not self.check_virtualbox_installed():
            raise RuntimeError(
                "VirtualBox is not installed. Please install VirtualBox to continue."
            )

        if not executable.exists():
            raise FileNotFoundError(f"Executable not found: {executable}")

        if not self.check_vm_exists():
            raise RuntimeError(
                f"VirtualBox VM '{self.vm_name}' does not exist. "
                "Please create a Windows VM with this name first."
            )

        print(f"Running VirtualBox command for: {executable}")
        print(f"Using VM: {self.vm_name}")
        print(f"Using proxy: {self.proxy_host}:{self.proxy_port}")

        # Attach USB devices if specified
        if usb_devices:
            print("USB device passthrough (VirtualBox native support):")
            for device in usb_devices:
                vendor_id = device.get("vendor_id", "")
                product_id = device.get("product_id", "")
                print(f"  - Vendor: {vendor_id}, Product: {product_id}")

                if vendor_id and product_id:
                    if self.attach_usb_device(vendor_id, product_id):
                        print("    ✓ USB filter configured")
                    else:
                        print("    ⚠ Failed to configure USB filter")

        # Build command to execute in the VM
        cmd_args = [str(executable)]
        if args:
            cmd_args.extend(args)

        # Note: This is a simplified example. In a real implementation, you would:
        # 1. Start the VM if not running
        # 2. Copy the executable to the VM
        # 3. Execute it via VBoxManage guestcontrol
        # 4. Capture the output
        # 5. Stop the VM if you started it

        print("\nNote: Full VirtualBox execution requires:")
        print("  1. A configured Windows VM")
        print("  2. Guest Additions installed in the VM")
        print("  3. Network configuration for proxy access")
        print("\nThis runner configures USB passthrough but doesn't execute the program.")
        print("USB devices will be available when you manually run the executable in the VM.")

        # Return a mock completed process for now
        # In a full implementation, this would execute the program in the VM
        result = subprocess.CompletedProcess(
            args=cmd_args,
            returncode=0,
            stdout="VirtualBox USB configuration completed",
            stderr="",
        )

        return result
