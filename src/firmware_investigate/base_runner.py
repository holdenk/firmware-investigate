"""Base class for all executable runners."""

import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional


class BaseRunner(ABC):
    """Abstract base class for runners that execute programs."""

    def __init__(self, proxy_host: str = "127.0.0.1", proxy_port: int = 8080):
        """Initialize the base runner.

        Args:
            proxy_host: Proxy server host for network interception.
            proxy_port: Proxy server port for network interception.
        """
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

    @abstractmethod
    def run(
        self,
        executable: Path,
        args: Optional[List[str]] = None,
        usb_devices: Optional[List[Dict[str, str]]] = None,
    ) -> subprocess.CompletedProcess:
        """Run an executable.

        Args:
            executable: Path to the executable.
            args: Optional command-line arguments for the executable.
            usb_devices: Optional list of USB devices to pass through
                        (format: [{"vendor_id": "0x2685", "product_id": "0x0900"}]).

        Returns:
            CompletedProcess object from subprocess.run.

        Raises:
            FileNotFoundError: If executable doesn't exist or runner is not available.
            RuntimeError: If execution fails.
        """
        pass
