"""Module for running macOS executables directly."""

import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from firmware_investigate.base_runner import BaseRunner


class MacOSRunner(BaseRunner):
    """Runner for executing macOS programs directly with user confirmation.

    Note: This runner runs programs on the native macOS system. It requires
    user confirmation before executing any commands.
    """

    def check_macos(self) -> bool:
        """Check if running on macOS.

        Returns:
            True if running on macOS, False otherwise.
        """
        return platform.system() == "Darwin"

    def run(
        self,
        executable: Path,
        args: Optional[List[str]] = None,
        usb_devices: Optional[List[Dict[str, str]]] = None,
    ) -> subprocess.CompletedProcess:
        """Run a macOS executable directly after user confirmation.

        Args:
            executable: Path to the macOS executable (.pkg, .dmg, or .app).
            args: Optional command-line arguments for the executable.
            usb_devices: Optional list of USB devices (informational only for macOS).

        Returns:
            CompletedProcess object from subprocess.run.

        Raises:
            FileNotFoundError: If executable doesn't exist.
            RuntimeError: If not running on macOS or if user denies execution.
        """
        if not self.check_macos():
            raise RuntimeError(
                "MacOSRunner can only be used on macOS. "
                "Current platform: {}".format(platform.system())
            )

        if not executable.exists():
            raise FileNotFoundError(f"Executable not found: {executable}")

        print(f"\nPreparing to run macOS executable: {executable}")
        print(f"File type: {executable.suffix}")

        if usb_devices:
            print("\nUSB devices (will be available to the application):")
            for device in usb_devices:
                vendor_id = device.get("vendor_id", "")
                product_id = device.get("product_id", "")
                print(f"  - Vendor: {vendor_id}, Product: {product_id}")

        # Determine the appropriate command based on file type
        if executable.suffix == ".pkg":
            cmd = ["open", str(executable)]
            cmd_description = "Open the .pkg installer"
        elif executable.suffix == ".dmg":
            cmd = ["open", str(executable)]
            cmd_description = "Open the .dmg disk image"
        elif executable.suffix == ".app" or executable.is_dir():
            cmd = ["open", str(executable)]
            cmd_description = "Open the application"
        else:
            # Try to execute directly
            cmd = [str(executable)]
            if args:
                cmd.extend(args)
            cmd_description = "Execute the file directly"

        # Display the command and ask for confirmation
        print("\n" + "=" * 60)
        print("CONFIRMATION REQUIRED")
        print("=" * 60)
        print(f"Command: {' '.join(cmd)}")
        print(f"Action: {cmd_description}")
        print("\nThis will run the executable on your macOS system.")
        print("=" * 60)

        try:
            response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
        except EOFError:
            # Handle non-interactive environments
            response = "no"

        if response not in ["yes", "y"]:
            raise RuntimeError("User declined to run the executable")

        print("\n✓ User confirmed. Executing command...")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )

            print(f"Execution completed with exit code: {result.returncode}")

            if result.stdout:
                print(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"STDERR:\n{result.stderr}")

            return result

        except Exception as e:
            raise RuntimeError(f"Failed to run macOS executable: {e}")
