"""Cardo firmware downloader."""

from typing import Optional

from .base import BaseDownloader


class CardoDownloader(BaseDownloader):
    """Downloader for Cardo firmware update tools."""

    # Direct download URLs for Cardo Updater
    CARDO_WINDOWS_URL = "https://update.cardosystems.com/cardo-app/cardo_updater_win_latest.exe"
    CARDO_MACOS_URL = (
        "https://update.cardosystems.com/cardo-app/" "CardoUpdateLite_OTA_darwin_arm64_latest.dmg"
    )
    # Upstream source to check if download fails
    CARDO_UPSTREAM_URL = "https://cardo.htskys.com/en/support/upadate-firmware/"

    def __init__(self, working_dir: str = "working", platform_override: Optional[str] = None):
        """Initialize Cardo downloader.

        Args:
            working_dir: Directory where downloaded files will be stored.
            platform_override: Override platform detection (windows, darwin).
        """
        super().__init__(working_dir, platform_override)

    def get_url(self) -> str:
        """Get the download URL for Cardo firmware tools.

        Returns:
            The URL to download from based on platform.
        """
        if self.platform == "windows":
            return self.CARDO_WINDOWS_URL
        elif self.platform == "darwin":
            return self.CARDO_MACOS_URL
        else:
            # Default to Windows if platform not recognized
            return self.CARDO_WINDOWS_URL

    def get_filename(self) -> str:
        """Get the filename for the Cardo download.

        Returns:
            The filename to save as based on platform.
        """
        if self.platform == "windows":
            return "cardo_updater_win_latest.exe"
        elif self.platform == "darwin":
            return "CardoUpdateLite_OTA_darwin_arm64_latest.dmg"
        else:
            # Default to Windows if platform not recognized
            return "cardo_updater_win_latest.exe"
