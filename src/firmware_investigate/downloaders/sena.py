"""Sena firmware downloader."""

from typing import Optional

from .base import BaseDownloader


class SenaDownloader(BaseDownloader):
    """Downloader for Sena firmware update tools."""

    # Direct download URLs for Sena Device Manager
    SENA_WINDOWS_URL = (
        "https://firmware.sena.com/senabluetoothmanager/"
        "SenaDeviceManagerForWindows-v4.4.16-setup_x64.exe"
    )
    SENA_MACOS_URL = (
        "https://firmware.sena.com/senabluetoothmanager/" "SENADeviceManagerForMAC-v4.4.16.pkg"
    )
    # Upstream source to check if download fails
    SENA_UPSTREAM_URL = "https://www.sena.com/en-us/support/device-manager/"

    def __init__(self, working_dir: str = "working", platform_override: Optional[str] = None):
        """Initialize Sena downloader.

        Args:
            working_dir: Directory where downloaded files will be stored.
            platform_override: Override platform detection (windows, darwin).
        """
        super().__init__(working_dir, platform_override)

    def get_url(self) -> str:
        """Get the download URL for Sena firmware tools.

        Returns:
            The URL to download from based on platform.
        """
        if self.platform == "windows":
            return self.SENA_WINDOWS_URL
        elif self.platform == "darwin":
            return self.SENA_MACOS_URL
        else:
            # Default to Windows if platform not recognized
            return self.SENA_WINDOWS_URL

    def get_filename(self) -> str:
        """Get the filename for the Sena download.

        Returns:
            The filename to save as based on platform.
        """
        if self.platform == "windows":
            return "SenaDeviceManagerForWindows-v4.4.16-setup_x64.exe"
        elif self.platform == "darwin":
            return "SENADeviceManagerForMAC-v4.4.16.pkg"
        else:
            # Default to Windows if platform not recognized
            return "SenaDeviceManagerForWindows-v4.4.16-setup_x64.exe"
