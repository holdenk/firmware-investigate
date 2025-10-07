"""Motorola Defy firmware downloader."""

from typing import Optional

from .base import BaseDownloader


class MotorolaDownloader(BaseDownloader):
    """Downloader for Motorola Defy Satellite firmware update tools."""

    # Direct download URLs for Motorola Defy Satellite updater
    # Note: These URLs are for the Motorola Defy Satellite Link firmware updater
    MOTOROLA_WINDOWS_URL = (
        "https://motorola-global-portal-pit.custhelp.com/euf/assets/software/"
        "MotDefySatelliteLinkManager_Setup.exe"
    )
    MOTOROLA_MACOS_URL = (
        "https://motorola-global-portal-pit.custhelp.com/euf/assets/software/"
        "MotDefySatelliteLinkManager.dmg"
    )
    # Upstream source to check if download fails
    MOTOROLA_UPSTREAM_URL = "https://en-us.support.motorola.com/app/answers/detail/a_id/157173"

    def __init__(self, working_dir: str = "working", platform_override: Optional[str] = None):
        """Initialize Motorola downloader.

        Args:
            working_dir: Directory where downloaded files will be stored.
            platform_override: Override platform detection (windows, darwin).
        """
        super().__init__(working_dir, platform_override)

    def get_url(self) -> str:
        """Get the download URL for Motorola firmware tools.

        Returns:
            The URL to download from based on platform.
        """
        if self.platform == "windows":
            return self.MOTOROLA_WINDOWS_URL
        elif self.platform == "darwin":
            return self.MOTOROLA_MACOS_URL
        else:
            # Default to Windows if platform not recognized
            return self.MOTOROLA_WINDOWS_URL

    def get_filename(self) -> str:
        """Get the filename for the Motorola download.

        Returns:
            The filename to save as based on platform.
        """
        if self.platform == "windows":
            return "MotDefySatelliteLinkManager_Setup.exe"
        elif self.platform == "darwin":
            return "MotDefySatelliteLinkManager.dmg"
        else:
            # Default to Windows if platform not recognized
            return "MotDefySatelliteLinkManager_Setup.exe"
