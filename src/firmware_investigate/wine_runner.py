"""Module for running Windows executables using Wine."""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class WineRunner:
    """Runner for executing Windows programs using Wine."""

    def __init__(
        self,
        wine_prefix: Optional[Path] = None,
        proxy_host: str = "127.0.0.1",
        proxy_port: int = 8080,
    ):
        """Initialize the Wine runner.

        Args:
            wine_prefix: Custom WINEPREFIX directory.
            proxy_host: Proxy server host for network interception.
            proxy_port: Proxy server port for network interception.
        """
        self.wine_prefix = wine_prefix or Path.home() / ".wine-firmware-investigate"
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

    def setup_environment(self) -> Dict[str, str]:
        """Setup Wine environment variables.

        Returns:
            Dictionary of environment variables for Wine.
        """
        env = os.environ.copy()
        env["WINEPREFIX"] = str(self.wine_prefix)
        
        # Configure proxy settings for Wine
        proxy_url = f"http://{self.proxy_host}:{self.proxy_port}"
        env["http_proxy"] = proxy_url
        env["https_proxy"] = proxy_url
        
        # Wine debug settings (reduce noise)
        env["WINEDEBUG"] = "-all"
        
        return env

    def check_wine_installed(self) -> bool:
        """Check if Wine is installed.

        Returns:
            True if Wine is available, False otherwise.
        """
        try:
            subprocess.run(
                ["wine", "--version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def run(
        self,
        executable: Path,
        args: Optional[List[str]] = None,
        usb_devices: Optional[List[Dict[str, str]]] = None,
    ) -> subprocess.CompletedProcess:
        """Run a Windows executable using Wine.

        Args:
            executable: Path to the Windows executable.
            args: Optional command-line arguments for the executable.
            usb_devices: Optional list of USB devices to pass through
                        (format: [{"vendor_id": "0x2685", "product_id": "0x0900"}]).

        Returns:
            CompletedProcess object from subprocess.run.

        Raises:
            FileNotFoundError: If executable doesn't exist or Wine is not installed.
            RuntimeError: If Wine execution fails.
        """
        if not self.check_wine_installed():
            raise RuntimeError("Wine is not installed. Please install Wine to continue.")

        if not executable.exists():
            raise FileNotFoundError(f"Executable not found: {executable}")

        # Create Wine prefix if it doesn't exist
        self.wine_prefix.mkdir(parents=True, exist_ok=True)

        # Setup environment
        env = self.setup_environment()

        # Build command
        cmd = ["wine", str(executable)]
        if args:
            cmd.extend(args)

        print(f"Running Wine command: {' '.join(cmd)}")
        print(f"Using WINEPREFIX: {self.wine_prefix}")
        print(f"Using proxy: {self.proxy_host}:{self.proxy_port}")

        if usb_devices:
            print("USB device passthrough:")
            for device in usb_devices:
                vendor_id = device.get("vendor_id", "")
                product_id = device.get("product_id", "")
                print(f"  - Vendor: {vendor_id}, Product: {product_id}")
            print("Note: USB passthrough requires additional Wine/QEMU configuration")

        try:
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
            )
            
            print(f"Wine execution completed with exit code: {result.returncode}")
            
            if result.stdout:
                print(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"STDERR:\n{result.stderr}")
            
            return result

        except Exception as e:
            raise RuntimeError(f"Failed to run Wine: {e}")
